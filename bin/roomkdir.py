#!/usr/bin/python

# ROOT command line tools: roomkdir
# Author: Julien Ripoche
# Mail: julien.ripoche@u-psud.fr
# Date: 13/08/15

"""Command line to add directories in ROOT files"""

from cmdLineUtils import *

MKDIR_ERROR = "cannot create directory '{0}'"

def createDirectories(rootFile,pathSplit,optDict):
    """Same behaviour as createDirectory but allows the possibility
    to build an whole path recursively with opt_dict["parents"]"""
    if pathSplit == []:
        pass
    elif optDict["parents"]:
        for i in range(len(pathSplit)):
            currentPathSplit = pathSplit[:i+1]
            if not (isExisting(rootFile,currentPathSplit) \
                and isDirectory(rootFile,currentPathSplit)):
                createDirectory(rootFile,currentPathSplit)
    else:
        doMkdir = True
        for i in range(len(pathSplit)-1):
            currentPathSplit = pathSplit[:i+1]
            if not (isExisting(rootFile,currentPathSplit) \
                and isDirectory(rootFile,currentPathSplit)):
                doMkdir = False
                break
        if doMkdir:
            createDirectory(rootFile,pathSplit)
        else:
            logging.warning(MKDIR_ERROR.format("/".join(pathSplit)))

# Help strings
COMMAND_HELP = \
    "Add directories in a ROOT files " + \
    "(for more informations please look at the man page)."
PARENT_HELP = \
    "make parent directories as needed, no error if existing."

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=COMMAND_HELP)
parser.add_argument("sourcePatternList", help=SOURCES_HELP, nargs='+')
parser.add_argument("-p", "--parents", help=PARENT_HELP, action="store_true")
args = parser.parse_args()

# Create a list of tuples that contain source ROOT file names
# and lists of path in these files
sourceList = \
    [tup for pattern in args.sourcePatternList \
    for tup in patternToFileNameAndPathSplitList(pattern,wildcards=False)]

# Create a dictionnary with options
optDict = vars(args)

# Loop on the ROOT files
for fileName, pathSplitList in sourceList:
    with stderrRedirected():
        rootFile = ROOT.TFile(fileName,"update")
    createDirectories(rootFile,pathSplitList[0],optDict)
    rootFile.Close()
