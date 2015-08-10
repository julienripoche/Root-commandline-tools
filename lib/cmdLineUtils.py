#!/usr/bin/python

"""Contain utils for ROOT command line tools"""

from redirectEscapeCharacters import *
# redirect output (escape characters during ROOT importation...)
with stdoutRedirected():
    import ROOT

from getTerminalSize import *
import argparse
import glob
import os
import sys
import fnmatch
import logging

def changeDirectory(rootFile,pathSplit):
    """Change the current directory (ROOT.gDirectory)
    by the corresponding directory (rootFile,pathSplit)"""
    rootFile.cd()
    for directoryName in pathSplit:
        ROOT.gDirectory.Get(directoryName).cd()
        #directory = ROOT.gDirectory.Get(directoryName)
        #if hasattr(directory,"cd"):
        #    directory.cd()
        #else:
        #    logging.error("There is no directory named \"{0}\"" \
        #                  .format(directoryName))
        #    break

def getKey(rootFile,pathSplit):
    """Get the key of the corresponding object
    (rootFile,pathSplit)"""
    changeDirectory(rootFile,pathSplit[:-1])
    return ROOT.gDirectory.GetKey(pathSplit[-1])

def isDirectoryKey(key):
    """Return True if the object, corresponding to the key,
    inherits from TDirectory, False if not"""
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())

def isDirectory(rootFile,pathSplit):
    """Return True if the object, corresponding to (rootFile,pathSplit),
    inherits from TDirectory, False if not"""
    if pathSplit == []: return True # the object is the rootFile itself
    else: return isDirectoryKey(getKey(rootFile,pathSplit))

def isTreeKey(key):
    """Return True if the object, corresponding to the key,
    inherits from TTree, False if not"""
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())

def isTree(rootFile,pathSplit):
    """Return True if the object, corresponding to (rootFile,pathSplit),
    inherits from TTree, False if not"""
    if pathSplit == []: return False # the object is the rootFile itself
    else: return isTreeKey(getKey(rootFile,pathSplit))

def getKeyList(rootFile,pathSplit):
    """Get the list of key of the directory (rootFile,pathSplit),
    if (rootFile,pathSplit) is not a directory then get the key"""
    if isDirectory(rootFile,pathSplit):
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
        elif isDirectory(rootFile,pathSplit): dirList.append(pathSplit)
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
    with stderrRedirected():
        rootFile = ROOT.TFile.Open(fileName)
    pathSplitList = [[]]
    for patternPiece in patternSplit:
        newPathSplitList = []
        for pathSplit in pathSplitList:
            ## Stay in top level of trees
            #if isTree(rootFile,pathSplit[:-1]):
            #    continue
            #elif isDirectory(rootFile,pathSplit):
            if isDirectory(rootFile,pathSplit):
                changeDirectory(rootFile,pathSplit)
                newPathSplitList.extend( \
                    [pathSplit + [key.GetName()] \
                    for key in ROOT.gDirectory.GetListOfKeys() \
                    if fnmatch.fnmatch(key.GetName(),patternPiece)])
            ## Equivalent for tree inspection
            #elif isTree(rootFile,pathSplit):
            #    changeDirectory(rootFile,pathSplit[:-1])
            #    T = ROOT.gDirectory.Get(pathSplit[-1])
            #    newPathSplitList.extend( \
            #        [pathSplit + [branch.GetName()] \
            #        for branch in T.GetListOfBranches() \
            #        if fnmatch.fnmatch(branch.GetName(),patternPiece)])
        pathSplitList = newPathSplitList
    if pathSplitList == []: # no match
        logging.warning("Can't find {0} in {1}".format(pattern,fileName))
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

def isExist(rootFile,pathSplit):
    """..."""
    changeDirectory(rootFile,pathSplit[:-1])
    return ROOT.gDirectory.GetListOfKeys().Contains(pathSplit[-1])

def copyRootObject(sourceFile,sourcePathSplit,destFile,destPathSplit,oneFile=False):
    """Create the destination directory, if needed,
    and then run copyRootObjectRecursive"""
    setName = ""
    if oneFile and destPathSplit != [] and not isExist(destFile,destPathSplit):
        setName = destPathSplit[-1]
    if sourcePathSplit != []:
        key = getKey(sourceFile,sourcePathSplit)
        if isDirectoryKey(key):
            if setName != "":
                changeDirectory(destFile,destPathSplit[:-1])
                ROOT.gDirectory.mkdir(setName)
                copyRootObjectRecursive(sourceFile,sourcePathSplit, \
                    destFile,destPathSplit)
            else:
                changeDirectory(destFile,destPathSplit)
                if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                    ROOT.gDirectory.mkdir(key.GetName())
                copyRootObjectRecursive(sourceFile,sourcePathSplit, \
                    destFile,destPathSplit+[key.GetName()])
        else:
            if setName != "":  
                copyRootObjectRecursive(sourceFile,sourcePathSplit, \
                    destFile,destPathSplit[:-1],setName)
            else:
                copyRootObjectRecursive(sourceFile,sourcePathSplit, \
                    destFile,destPathSplit)
    else:
        copyRootObjectRecursive(sourceFile,sourcePathSplit, \
            destFile,destPathSplit)

def copyRootObjectRecursive(sourceFile,sourcePathSplit,destFile,destPathSplit,setName=""):
    """Copy objects from a file or directory (sourceFile,sourcePathSplit)
    to an other file or directory (destFile,destPathSplit)
    - that's a recursive function
    - Python adaptation of a root input/output tutorial :
      $ROOTSYS/tutorials/io/copyFiles.C"""
    for key in getKeyList(sourceFile,sourcePathSplit):
        if isDirectoryKey(key):
            changeDirectory(destFile,destPathSplit)
            if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                ROOT.gDirectory.mkdir(key.GetName())
            copyRootObjectRecursive(sourceFile,sourcePathSplit+[key.GetName()], \
                destFile,destPathSplit+[key.GetName()])
        elif isTreeKey(key):
            T = key.GetMotherDir().Get(key.GetName()+";"+str(key.GetCycle()))
            changeDirectory(destFile,destPathSplit)
            newT = T.CloneTree(-1,"fast")
            if setName != "":
                newT.SetName(setName)
            newT.Write()
        else:
            obj = key.ReadObj()
            changeDirectory(destFile,destPathSplit)
            ## Option replace if existing ?
            #if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
            #    ROOT.gDirectory.Delete(obj.GetName()+";*")
            if setName != "":
                obj.SetName(setName)
            obj.Write()
            obj.Delete()
    changeDirectory(destFile,destPathSplit)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)

def deleteRootObject(rootFile,pathSplit,optDict):
    """Remove the object (rootFile,pathSplit)
    -i prompt before every removal"""
    answer = 'y'
    if optDict['i']: answer = \
       raw_input("Are you sure to remove '{0}' from '{1}' ? (y/n) : " \
                 .format("/".join(pathSplit),rootFile.GetName())) \
       if pathSplit != [] else \
       raw_input("Are you sure to remove '{0}' ? (y/n) : " \
                 .format(rootFile.GetName()))
    if answer.lower() == 'y':
        if pathSplit != []:
            changeDirectory(rootFile,pathSplit[:-1])
            ROOT.gDirectory.Delete(pathSplit[-1]+";*")
        else:
            rootFile.Close()
            os.remove(rootFile.GetName())

# Help strings for ROOT command line tools

SOURCE_HELP = \
    "path of the source."
SOURCES_HELP = \
    "path of the source(s)."
DEST_HELP = \
    "path of the destination."

ROOBROWSE_HELP = \
    "Open a ROOT file on a TBrowser " + \
    "(for more informations please look at the man page)."
ROOEVENTSELECTOR_HELP = \
    "Copy subsets of trees from source ROOT files " + \
    "to new trees on a destination ROOT file " + \
    "(for more informations please look at the man page)."
ROOCP_HELP = \
    "Copy objects from ROOT files into an other " + \
    "(for more informations please look at the man page)."
ROOLS_HELP = \
    "Display ROOT files contents in the terminal " + \
    "(for more informations please look at the man page)."
ROOMKDIR_HELP = \
    "Add directories in a ROOT files " + \
    "(for more informations please look at the man page)."
ROOMV_HELP = \
    "Move objects from ROOT files to an other " + \
    "(for more informations please look at the man page)."
ROOPRINT_HELP = \
    "Print ROOT files contents on ps,pdf or pictures files " + \
    "(for more informations please look at the man page)."
ROORM_HELP = \
    "Remove objects from ROOT files " + \
    "(for more informations please look at the man page)."

COMPRESS_HELP = \
    "change the compression settings of the destination file."
DIRECTORY_HELP = \
    "put output files in a subdirectory named DIRECTORY."
FIRST_EVENT_HELP = \
    "specify the first event to copy."
FORMAT_HELP = \
    "specify output format (ex: pdf, png)."
I_HELP = \
    "prompt before every removal."
LAST_EVENT_HELP = \
    "specify the last event to copy."
LONG_PRINT_HELP = \
    "use a long listing format."
OUTPUT_HELP = \
    "merge files in a file named OUTPUT (only for ps and pdf)."
PARENT_HELP = \
    "make parent directories as needed, no error if existing."
RECREATE_HELP = \
    "recreate the destination file."
TREE_PRINT_HELP = \
    "print tree recursively and use a long listing format."
