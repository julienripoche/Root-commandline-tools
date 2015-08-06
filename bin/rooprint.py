#!/usr/bin/python

"""Command line to print ROOT files contents on ps,pdf or png,gif..."""

from cmdLineUtils import *
from cmdLineHelps import *

extensionList = ["ps","Portrait","Landscape","eps","Preview", \
                "pdf","svg","tex","gif","xpm","png","jpg"]

# Check the use of os.path
# Think of print message like "pdf file is created"
                
##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=ROOPRINT_HELP)
parser.add_argument("sourcePatternList", help=SOURCES_HELP, nargs='+')
parser.add_argument("-d", "--directory", help=DIRECTORY_HELP)
parser.add_argument("-m", "--merge", help=MERGE_HELP)
parser.add_argument("-e", "--extension", help=EXTENSION_HELP)
args = parser.parse_args()

# Create a list of tuples that contain source ROOT file names
# and lists of path in these files
sourceList = \
    [tup for pattern in args.sourcePatternList \
    for tup in patternToFileNameAndPathSplitList(pattern)]

# Create a dictionnary with options
optDict = vars(args)
del optDict["sourcePatternList"]

# Initialize the canvas
ROOT.gErrorIgnoreLevel = 9999
ROOT.gROOT.SetBatch()
canvas = ROOT.TCanvas("canvas")

# Take the extension of output file (merge option)
if not optDict["extension"] and optDict["merge"]:
    fileName = optDict["merge"]
    extension = fileName.split(".")[-1]
    if extension in extensionList: optDict["extension"] = extension

# Use pdf as default extension
if not optDict["extension"]: optDict["extension"] = "pdf"

# Create the output directory (directory option)
if optDict["directory"]:
    if not os.path.isdir(os.path.join(os.getcwd(),optDict["directory"])):
        os.mkdir(optDict["directory"])

# Make the output name, begin to print (merge option)
if optDict["merge"]:
    if optDict["extension"] in ['ps','pdf']:
        outputFileName = optDict["merge"]
        if optDict["directory"]: outputFileName = \
           optDict["directory"] + "/" + outputFileName
        canvas.Print(outputFileName+"[",optDict["extension"])
    else:
        print("Can't merge pictures, only postscript or pdf files")
        optDict["output"] = ""

# Loop on the root files
for fileName, pathSplitList in sourceList:
    with stderrRedirected():
        rootFile = ROOT.TFile.Open(fileName)
    # Fill the key list (almost the same as in rools)
    objList,dirList = typeSelector(rootFile,pathSplitList)
    keyList = [getKey(rootFile,pathSplit) for pathSplit in objList]
    keyList.sort()
    dirList.sort()
    for pathSplit in dirList: keyList.extend(getKeyList(rootFile,pathSplit))
    keyList = [key for key in keyList if not isDirectoryKey(key)]
    for key in keyList:
        if isTreeKey(key):
            obj = key.ReadObj()
            for branch in obj.GetListOfBranches():
                if not optDict["merge"]:
                    outputFileName = \
                        branch.GetName() + "." +optDict["extension"]
                    if optDict["directory"]:
                        print "Here, use os.path !"
                        outputFileName = \
                            optDict["directory"] + "/" + outputFileName
                obj.Draw(branch.GetName())
                if optDict["merge"] or optDict["extension"] == 'pdf':
                    objTitle = "Title:"+branch.GetName()+" : "+branch.GetTitle()
                    canvas.Print(outputFileName,objTitle)
                else:
                    canvas.Print(outputFileName,optDict["extension"])
        else:
            if not optDict["merge"]:
                outputFileName = key.GetName() + "." +optDict["extension"]
                if optDict["directory"]:
                    print "Here, use os.path !"
                    outputFileName = \
                        optDict["directory"] + "/" + outputFileName
            obj = key.ReadObj()
            obj.Draw()
            if optDict["merge"] or optDict["extension"] == 'pdf':
                objTitle = "Title:"+key.GetClassName()+" : "+key.GetTitle()
                canvas.Print(outputFileName,objTitle)
            else:
                canvas.Print(outputFileName,optDict["extension"])
    rootFile.Close()

# End to print (merge option)
if optDict["merge"]:
    canvas.Print(outputFileName+"]",objTitle)
