#!/usr/bin/python

"""Contain utils for ROOT commandlines tools"""

from redirectEscapeCharacters import *
# redirect output (escape characters during ROOT importation...)
with stdoutRedirected(to=os.devnull), mergedStderrStdout():
    import ROOT

from getTerminalSize import *
import argparse
import glob
import os
import sys
import fnmatch

def changeDirectory(rootFile,pathSplit):
    """Change the current directory (ROOT.gDirectory)
    by the corresponding directory (rootFile,pathSplit)"""
    rootFile.cd()
    for directoryName in pathSplit: ROOT.gDirectory.Get(directoryName).cd()

def getKey(rootFile,pathSplit):
    """Get the key of the corresponding object
    (rootFile,pathSplit)"""
    changeDirectory(rootFile,pathSplit[:-1])
    return ROOT.gDirectory.GetKey(pathSplit[-1])

def isDirectory(key):
    """Return True if the object (corresponding to key)
    inherits from TDirectory, False if not"""
    if type(key) != ROOT.TKey: # received (rootFile,pathSplit) instead of a key
        rootFile,pathSplit = key
        if pathSplit == []: return True # the object is the rootFile itself
        else: key = getKey(rootFile,pathSplit)
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())

def isTree(key):
    """Return True if the object (corresponding to key)
    inherits from TTree, False if not"""
    if type(key) != ROOT.TKey: # received (rootFile,pathSplit) instead of a key
        rootFile,pathSplit = key
        if pathSplit == []: return False # the object is the rootFile itself
        else: key = getKey(rootFile,pathSplit)
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())

def getKeyList(rootFile,pathSplit):
    """Get the list of key of the directory (rootFile,pathSplit),
    if (rootFile,pathSplit) is not a directory then get the key"""
    if isDirectory((rootFile,pathSplit)):
        changeDirectory(rootFile,pathSplit)
        return ROOT.gDirectory.GetListOfKeys()
    else: return [getKey(rootFile,pathSplit)]

def typeSelector(rootFile,pathSplitList):
    """Separate directories and other objects
    for rools and rooprint"""
    objList = []
    dirList = []
    for pathSplit in pathSplitList:
        if pathSplit == []: dirList.append(pathSplit)
        elif isDirectory((rootFile,pathSplit)): dirList.append(pathSplit)
        else: objList.append(pathSplit)
    return objList,dirList

def patternToPathSplitList(fileName,pattern):
    """Get the list of pathSplit of objects in the ROOT file
    corresponding to fileName that match with the pattern"""
    # avoid multiple slash problem
    patternSplit = [n for n in pattern.split("/") if n != ""]
    # whole ROOT file, so unnecessary to open it
    if patternSplit == []: return [[]]
    # redirect output (missing dictionary for class...)
    with stdoutRedirected(to=os.devnull), mergedStderrStdout():
        rootFile = ROOT.TFile.Open(fileName)
    pathSplitList = [[]]
    for patternPiece in patternSplit:
        newPathSplitList = []
        for pathSplit in pathSplitList:
            # security to stay in top level of trees
            if isTree((rootFile,pathSplit[:-1])): continue
            elif isDirectory((rootFile,pathSplit)):
                changeDirectory(rootFile,pathSplit)
                newPathSplitList.extend( \
                    [pathSplit + [key.GetName()] \
                    for key in ROOT.gDirectory.GetListOfKeys() \
                    if fnmatch.fnmatch(key.GetName(),patternPiece)])
            elif isTree((rootFile,pathSplit)):
                changeDirectory(rootFile,pathSplit[:-1])
                T = ROOT.gDirectory.Get(pathSplit[-1])
                newPathSplitList.extend( \
                    [pathSplit + [branch.GetName()] \
                    for branch in T.GetListOfBranches() \
                    if fnmatch.fnmatch(branch.GetName(),patternPiece)])
        pathSplitList = newPathSplitList
    if pathSplitList == []: # no match
        print("patternToPathSplitList : can't find {0} in {1}" \
              .format(pattern,fileName))
    return pathSplitList

def patternToFileNameAndPathSplitList(pattern,regexp = True):
    """Get the list of tuple containing both :
    - ROOT file name
    - list of path splited (in the corresponding file)
      of object that matches
    Use regular expression by default"""
    fileList = []
    patternSplit = pattern.split(":")
    if patternSplit[0] in ["http","https","ftp"]: # file from the web
        patternSplit[0] += ":"+patternSplit[1]
        del patternSplit[1]
        fileNameList = [patternSplit[0]]
    else: fileNameList = \
        [os.path.expandvars(os.path.expanduser(i)) \
        for i in glob.iglob(patternSplit[0])] \
        if regexp else \
        [os.path.expandvars(os.path.expanduser(patternSplit[0]))]
    for fileName in fileNameList:
        # there is a pattern of path in the ROOT file
        if len(patternSplit)>1 : pathSplitList = \
           patternToPathSplitList(fileName,patternSplit[1]) \
           if regexp else \
           [[n for n in patternSplit[1].split("/") if n != ""]]
        else: pathSplitList = [[]] # whole ROOT file
        fileList.append((fileName,pathSplitList))
    return fileList

def copyRootObject(sourceFile,sourcePathSplit,destFile,destPathSplit):
    """Copy objects from a file (sourceFile,sourcePathSplit)
    to a directory in an other file (destFile,destPathSplit)
    - that's a recursive function
    - Python adaptation of a root input/output tutorial :
      $ROOTSYS/tutorials/io/copyFiles.C"""
    for key in getKeyList(sourceFile,sourcePathSplit):
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if (not cl): return
        if (cl.InheritsFrom(ROOT.TDirectory.Class())):
            changeDirectory(destFile,destPathSplit)
            if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                ROOT.gDirectory.mkdir(key.GetName())
            changeDirectory(sourceFile,sourcePathSplit+[key.GetName()])
            copyRootObject(sourceFile,sourcePathSplit+[key.GetName()], \
                           destFile,destPathSplit+[key.GetName()])
        elif (cl.InheritsFrom(ROOT.TTree.Class())):
            changeDirectory(sourceFile,sourcePathSplit[:-1])
            T = ROOT.gDirectory.Get(key.GetName()+";"+str(key.GetCycle()))
            changeDirectory(destFile,destPathSplit)
            newT = T.CloneTree(-1,"fast")
            newT.Write()
        else:
            obj = key.ReadObj()
            changeDirectory(destFile,destPathSplit)
            # Option replace ?
            #if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
            #    ROOT.gDirectory.Delete(obj.GetName()+";*")
            obj.Write()
            del obj
    changeDirectory(destFile,destPathSplit)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)

def deleteRootObject(rootFile,pathSplit,optDict):
    """Remove the object (rootFile,pathSplit)
    - option force to avoid the confirmation"""
    answer = 'y'
    if not optDict['force']: answer = \
       raw_input("Are you sure to remove '{0}' from '{1}' ? (y/n) : " \
                 .format("/".join(pathSplit),rootFile.GetName())) \
       if pathSplit != [] else \
       raw_input("Are you sure to remove '{0}' ? (y/n) : " \
                 .format(rootFile.GetName()))
    if answer.lower() == 'y':
        if pathSplit != []:
            changeDirectory(rootFile,pathSplit[:-1])
            ROOT.gDirectory.Delete(pathSplit[-1]+";*")
        else: os.system("rm {}".format(rootFile.GetName()))
