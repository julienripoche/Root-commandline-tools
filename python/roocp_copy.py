#!/usr/bin/python

"""Commandline to copy an object from a root file to an other root file"""

from copy_dir import *
from dir_selector import *
import ROOT

def roocp_copy(source_file,source_path,dest_file,dest_path):
    key = get_key(source_file,source_path)
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    if (not cl):
        pass
    elif (cl.InheritsFrom(ROOT.TDirectory.Class())):
        chg_dir(source_file,source_path[:-1])
        subdir = ROOT.gDirectory.Get(source_path[-1]) # Get the TDirectory ...
        chg_dir(dest_file,dest_path)
        copy_dir(subdir)
        chg_dir(dest_file,dest_path)
    else :
        chg_dir(source_file,source_path[:-1])
        obj = key.ReadObj()
        chg_dir(dest_file,dest_path)
        obj.Write()
