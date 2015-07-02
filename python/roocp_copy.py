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
    if not ROOT.gDirectory.GetListOfKeys().Contains(source.GetName()):
        adir = savdir.mkdir(source.GetName())
    else :
        adir = ROOT.gDirectory.Get(source.GetName())
    adir.cd()
    # loop on all entries of this directory
    for key in source.GetListOfKeys():
        if is_directory(key):
            subdir = source.Get(key.GetName()) # Get the TDirectory...
            adir.cd()
            copy_dir(subdir)
            adir.cd()
        else:
            source.cd()
            obj = key.ReadObj()
            adir.cd()
            if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
                ROOT.gDirectory.Delete(obj.GetName()+";*")
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
        if is_directory(key):
            chg_dir(source_file,source_path[:-1])
            subdir = ROOT.gDirectory.Get(key.GetName()) # Get the TDirectory ...
            chg_dir(dest_file,dest_path)
            copy_dir(subdir)
            chg_dir(dest_file,dest_path)
        else :
            chg_dir(source_file,source_path[:-1])
            obj = key.ReadObj()
            chg_dir(dest_file,dest_path)
            if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
                ROOT.gDirectory.Delete(obj.GetName()+";*")
            obj.Write()
