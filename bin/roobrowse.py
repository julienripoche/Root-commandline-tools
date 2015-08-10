#!/usr/bin/python

"""Command line to open a ROOT file on a TBrowser"""

from cmdLineUtils import *

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=ROOBROWSE_HELP)
parser.add_argument("sourceName", nargs='?', help=SOURCE_HELP)
args = parser.parse_args()

if args.sourceName:
    with stderrRedirected():
        rootFile = ROOT.TFile.Open(args.sourceName)
    rootFile.Browse(ROOT.TBrowser())
    ROOT.PyROOT.TPyROOTApplication.Run(ROOT.gApplication)
    rootFile.Close()
else :
    browser = ROOT.TBrowser()
    ROOT.PyROOT.TPyROOTApplication.Run(ROOT.gApplication)
