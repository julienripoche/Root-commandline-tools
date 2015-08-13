#!/usr/bin/python

# ROOT command line tools: rooeventselector
# Author: Julien Ripoche
# Mail: julien.ripoche@u-psud.fr
# Date: 13/08/15

"""Command line to copy subsets of trees from source
ROOT files to new trees on a destination ROOT file"""

from cmdLineUtils import *

def copyTreeSubset(sourceFile,sourcePathSplit,destFile,destPathSplit,optDict):
    """Copy a subset of the tree from (sourceFile,sourcePathSplit)
    to (destFile,destPathSplit) according to options in optDict"""
    changeDirectory(sourceFile,sourcePathSplit[:-1])
    bigTree = ROOT.gDirectory.Get(sourcePathSplit[-1])
    nbrEntries = bigTree.GetEntries()
    # changeDirectory for the small tree not to be memory-resident
    changeDirectory(destFile,destPathSplit)
    smallTree = bigTree.CloneTree(0)
    firstOptionValue = optDict["first"]
    lastOptionValue = optDict["last"]
    firstEvent = \
        firstOptionValue \
        if firstOptionValue != None \
        else 0
    lastEvent = \
        lastOptionValue \
        if lastOptionValue != None and lastOptionValue < nbrEntries-1 \
        else nbrEntries-1
    for i in range(nbrEntries):
        if i >= firstEvent and i <= lastEvent:
            bigTree.GetEntry(i)
            smallTree.Fill()
    smallTree.Write()

# Help strings
COMMAND_HELP = \
    "Copy subsets of trees from source ROOT files " + \
    "to new trees on a destination ROOT file " + \
    "(for more informations please look at the man page)."
FIRST_EVENT_HELP = \
    "specify the first event to copy."
LAST_EVENT_HELP = \
    "specify the last event to copy."

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=COMMAND_HELP)
parser.add_argument("sourcePatternList", help=SOURCES_HELP, nargs='+')
parser.add_argument("destPattern", help=DEST_HELP)
parser.add_argument("-c","--compress", type=int, help=COMPRESS_HELP)
parser.add_argument("--recreate", help=RECREATE_HELP, action="store_true")
parser.add_argument("-f","--first", type=int, help=FIRST_EVENT_HELP)
parser.add_argument("-l","--last", type=int, help=LAST_EVENT_HELP)
args = parser.parse_args()

# Create a list of tuples that contain source ROOT file names
# and lists of path in these files
sourceList = \
    [tup for pattern in args.sourcePatternList \
    for tup in patternToFileNameAndPathSplitList(pattern)]

# Create a tuple that contain a destination ROOT file name
# and a path in this file
destList = \
    patternToFileNameAndPathSplitList( \
    args.destPattern,wildcards=False)
destFileName,destPathSplitList = destList[0]
destPathSplit = destPathSplitList[0]

# Create a dictionnary with options
optDict = vars(args)
compressOptionValue = optDict["compress"]

# Change the compression settings only on non existing file
if compressOptionValue != None and os.path.isfile(destFileName):
    logging.error("can't change compression settings on existing file")
    sys.exit()

# Creation of destination file (changing of the compression settings)
with stderrRedirected(): destFile = \
    ROOT.TFile(destFileName,"recreate") \
    if optDict["recreate"] else \
    ROOT.TFile(destFileName,"update")
if compressOptionValue != None: destFile.SetCompressionSettings(compressOptionValue)

# Loop on the root file
for sourceFileName, sourcePathSplitList in sourceList:
    with stderrRedirected(): sourceFile = \
        ROOT.TFile(sourceFileName) \
        if sourceFileName != destFileName else \
        destFile
    zombieExclusion(sourceFile)
    for sourcePathSplit in sourcePathSplitList:
        if isTree(sourceFile,sourcePathSplit): copyTreeSubset( \
            sourceFile,sourcePathSplit, \
            destFile,destPathSplit,optDict)
    if sourceFileName != destFileName:
        sourceFile.Close()
destFile.Close()
