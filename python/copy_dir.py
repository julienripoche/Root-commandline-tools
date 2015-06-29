#!/usr/bin/python

"""Python adaptation of a root input/output tutorial :
$ROOTSYS/tutorials/io/copyFiles.C"""

from is_directory import *
import ROOT

def copy_dir(source):
    # copy all objects and subdirs of directory source as a subdir of the current directory
    savdir = ROOT.gDirectory
    adir = savdir.mkdir(source.GetName())
    adir.cd()
    # loop on all entries of this directory
    for key in source.GetListOfKeys():
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if is_directory(key):
            subdir = source.Get(key.GetName()) # Get the TDirectory...
            adir.cd()
            copy_dir(subdir)
            adir.cd()
        else:
            source.cd()
            obj = key.ReadObj()
            adir.cd()
            obj.Write()
  
    adir.SaveSelf(ROOT.kTRUE)
    savdir.cd()
