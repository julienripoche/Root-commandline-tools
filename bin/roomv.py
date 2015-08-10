#!/usr/bin/python

"""Command line to move objects
from ROOT files to an other"""

from cmdLineUtils import *

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=ROOMV_HELP)
parser.add_argument("sourcePatternList", help=SOURCES_HELP, nargs='+')
parser.add_argument("destPattern", help=DEST_HELP)
parser.add_argument("-c","--compress", type=int, help=COMPRESS_HELP)
parser.add_argument("--recreate", help=RECREATE_HELP, action="store_true")
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
    args.destPattern,regexp=False)
destFileName,destPathSplitList = destList[0]
destPathSplit = destPathSplitList[0]

# Create a dictionnary with options
optDict = vars(args)
del optDict["sourcePatternList"]
del optDict["destPattern"]

# Creation of destination file (changing of the compression settings)
with stderrRedirected(): destFile = \
    ROOT.TFile.Open(destFileName,"recreate") \
    if optDict["recreate"] else \
    ROOT.TFile.Open(destFileName,"update")
if optDict["compress"]: destFile.SetCompressionSettings(optDict["compress"])
ROOT.gROOT.GetListOfFiles().Remove(destFile) # Fast copy necessity


# Loop on the root files
for sourceFileName, sourcePathSplitList in sourceList:
    with stderrRedirected(): sourceFile = \
        ROOT.TFile.Open(sourceFileName,"update") \
        if sourceFileName != destFileName else \
        destFile
    ROOT.gROOT.GetListOfFiles().Remove(sourceFile) # Fast copy necessity
    for sourcePathSplit in sourcePathSplitList:
        copyRootObject(sourceFile,sourcePathSplit,destFile,destPathSplit)
        deleteRootObject(sourceFile,sourcePathSplit,{'i':False})
    if sourceFileName != destFileName:
        sourceFile.Close()
destFile.Close()
