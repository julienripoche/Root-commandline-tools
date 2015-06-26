#!/usr/bin/python

"""Commandline to copy an object from a root file to an other root file"""

from copy_dir import *
from dir_selector import *
import ROOT

def roocp_copy(source_file,source_path,dest_file,dest_path):
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
