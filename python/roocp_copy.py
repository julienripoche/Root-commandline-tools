#!/usr/bin/python

"""Commandline to copy an object from a root file to an other root file"""

from utils import *
import ROOT

def copy_dir(source):
    """Python adaptation of a root input/output tutorial :
    $ROOTSYS/tutorials/io/copyFiles.C"""
    # copy all objects and subdirs of directory source
    # as a subdir of the current directory
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

def roocp_copy(source_file,source_path,dest_file,dest_path):
    """Copy an object from a root file to an other root file"""
    if source_path == []:
        key_list = get_key_list(source_file,source_path)
    else:
        key_list = [get_key(source_file,source_path)]

    for key in key_list:
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if (not cl):
            pass
        elif (cl.InheritsFrom(ROOT.TDirectory.Class())):
            chg_dir(source_file,source_path[:-1])
            subdir = ROOT.gDirectory.Get(key.GetName()) # Get the TDirectory ...
            chg_dir(dest_file,dest_path)
            copy_dir(subdir)
            chg_dir(dest_file,dest_path)
        else :
            chg_dir(source_file,source_path[:-1])
            obj = key.ReadObj()
            chg_dir(dest_file,dest_path)
            obj.Write()
