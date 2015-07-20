#!/usr/bin/python

"""Contain all utils for ROOT commandlines tools"""

# Redirection of escape characters during importations
from redirectEscapeCharacters import *
with stdoutRedirected(to=os.devnull), mergedStderrStdout():
    from getTerminalSize import *
    import ROOT
    import argparse
    import glob
    import os
    import sys
    import fnmatch

def changeDirectory(rootFile,pathSplit):
    """Change the current directory for
    (rootFile,pathSplit)"""
    rootFile.cd()
    for directoryName in pathSplit:
        ROOT.gDirectory.Get(directoryName).cd()

def getKey(rootFile,pathSplit):
    """Give the key of the corresponding object"""
    changeDirectory(rootFile,pathSplit[:-1])
    return ROOT.gDirectory.GetKey(pathSplit[-1])

def isDirectory(key):
    """Test if the object pointed by the key
    inherits from TDirectory"""
    # If function received (rootFile,pathSplit)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return True
        else:
            key = getKey(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())

def isTree(key):
    """Test if the object pointed by the key
    inherits from TTree"""
    # If function received (rootFile,pathSplit)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return False
        else:
            key = getKey(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())

def getKeyList(rootFile,pathSplit):
    """Give the list of key of the corresponding directory,
    if (rootFile,pathSplit) is not a directory give corresponding key"""
    if isDirectory((rootFile,pathSplit)):
        changeDirectory(rootFile,pathSplit)
        return ROOT.gDirectory.GetListOfKeys()
    else:
        return [getKey(rootFile,pathSplit)]

def typeSelector(rootFile,pathSplitList):
    """Separate directories, branches and other objects"""
    objList = []
    dirList = []
    for pathSplit in pathSplitList:
        if pathSplit == []:
            dirList.append(pathSplit)
        elif isTree((rootFile,pathSplit[:-1])):
            pass
        elif isDirectory((rootFile,pathSplit)):
            dirList.append(pathSplit)
        else:
            objList.append(pathSplit)
    return objList,dirList

def patternToPathSplitList(fileName,pattern):
    """Put in a list pathSplit of objects in the ROOT file
    corresponding to fileName that match with the pattern"""
    patternSplit = [n for n in pattern.split("/") if n != ""]
    # Full ROOT file, unnecessary but if not
    # then opening of rootFile for nothing...
    if patternSplit == []:
        return [[]]
    rootFile = ROOT.TFile.Open(fileName)
    pathSplitList = [[]]
    for patternPiece in patternSplit:
        newPathSplitList = []
        for pathSplit in pathSplitList:
            if isTree((rootFile,pathSplit[:-1])):
                # Security to stay in top level of trees
                continue
            elif isDirectory((rootFile,pathSplit)):
                changeDirectory(rootFile,pathSplit)
                newPathSplitList.extend([pathSplit + [key.GetName()]\
                                      for key in ROOT.gDirectory.GetListOfKeys()\
                                      if fnmatch.fnmatch(key.GetName(),patternPiece)])
            elif isTree((rootFile,pathSplit)):
                changeDirectory(rootFile,pathSplit[:-1])
                T = ROOT.gDirectory.Get(pathSplit[-1])
                newPathSplitList.extend([pathSplit + [branch.GetName()]\
                                      for branch in T.GetListOfBranches()\
                                      if fnmatch.fnmatch(branch.GetName(),patternPiece)])
        pathSplitList = newPathSplitList
    if pathSplitList == []:
        print("patternToPathSplitList : can't find {0} in {1}".format(pattern,fileName))
    return pathSplitList

def patternToFileNameAndPathSplitList(pattern,regexp = True):
    """Create a list of tuple which contain root fileName
    and pathSplitList in this file of object that matches"""
    fileList = []
    patternSplit = pattern.split(":")
    if patternSplit[0] in ["http","https","ftp"]:
        # File from the web
        patternSplit[0] += ":"+patternSplit[1]
        del patternSplit[1]
        fileNameList = [patternSplit[0]]
    else:
        if regexp:
            fileNameList = [os.path.expandvars(os.path.expanduser(i)) \
                         for i in glob.iglob(patternSplit[0])]
        else:
            fileNameList = [os.path.expandvars(os.path.expanduser( \
                            patternSplit[0]))]
    for fileName in fileNameList:
        if len(patternSplit)==2:
            # There is a pattern of path in the ROOT file
            if regexp:
                pathSplitList = patternToPathSplitList(fileName,patternSplit[1])
            else:
                pathSplitList = [[n for n in patternSplit[1].split("/") if n != ""]]
        else:
            # This is the entire ROOT file
            pathSplitList = [[]]
        fileList.append((fileName,pathSplitList))
    return fileList

def copyRootObject(sourceFile,sourcePathSplit,destinationFile,destinationPathSplit):
    """Python adaptation of a root input/output tutorial :
    $ROOTSYS/tutorials/io/copyFiles.C"""
    for key in getKeyList(sourceFile,sourcePathSplit):
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if (not cl):
            return
        if (cl.InheritsFrom(ROOT.TDirectory.Class())):
            changeDirectory(destinationFile,destinationPathSplit)
            if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                ROOT.gDirectory.mkdir(key.GetName())
            changeDirectory(sourceFile,sourcePathSplit+[key.GetName()])
            copyRootObject(sourceFile,sourcePathSplit+[key.GetName()],destinationFile,destinationPathSplit+[key.GetName()])
        elif (cl.InheritsFrom(ROOT.TTree.Class())):
            changeDirectory(sourceFile,sourcePathSplit[:-1])
            print "problem with cycles, don't forget to look at it..."
            T = ROOT.gDirectory.Get(key.GetName()+";1")
            changeDirectory(destinationFile,destinationPathSplit)
            newT = T.CloneTree(-1,"fast")
            newT.Write()
        else:
            obj = key.ReadObj()
            changeDirectory(destinationFile,destinationPathSplit)
            if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
                ROOT.gDirectory.Delete(obj.GetName()+";*")
            obj.Write()
            del obj

    changeDirectory(destinationFile,destinationPathSplit)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)

def deleteRootObject(rootFile,pathSplit,optDict):
    """Remove the object corresponding to the pathSplit
    from a ROOT file, option force to avoid the confirmation"""
    doRemove = True
    if not optDict['force']:
        if pathSplit != []:
            answer = raw_input("Are you sure to remove '{0}' from '{1}' ? (y/n) : " \
                                   .format("/".join(pathSplit),rootFile.GetName()))
        else:
            answer = raw_input("Are you sure to remove '{0}' ? (y/n) : " \
                                   .format(rootFile.GetName()))
        if answer.lower() != 'y':
            doRemovee = False
    if doRemove:
        if pathSplit != []:
            changeDirectory(rootFile,pathSplit[:-1])
            ROOT.gDirectory.Delete(pathSplit[-1]+";*")
        else:
            os.system("rm {}".format(rootFile.GetName()))
