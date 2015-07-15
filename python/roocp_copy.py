#!/usr/bin/python

"""Module which contain a function to copy objects from a root file to an other root file"""

from utils import *
import ROOT

def roocp_copy(source_file,source_path,dest_file,dest_path):
    """Python adaptation of a root input/output tutorial :
    $ROOTSYS/tutorials/io/copyFiles.C"""
        
    for key in get_key_list(source_file,source_path):
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if (not cl):
            return
        if (cl.InheritsFrom(ROOT.TDirectory.Class())):
            chg_dir(dest_file,dest_path)
            if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                ROOT.gDirectory.mkdir(key.GetName())
            chg_dir(source_file,source_path+[key.GetName()])
            roocp_copy(source_file,source_path+[key.GetName()],dest_file,dest_path+[key.GetName()])
        elif (cl.InheritsFrom(ROOT.TTree.Class())):
            chg_dir(source_file,source_path[:-1])
            T = ROOT.gDirectory.Get(key.GetName())
            chg_dir(dest_file,dest_path)
            newT = T.CloneTree(-1,"fast")
            newT.Write()
        else:
            obj = key.ReadObj()
            chg_dir(dest_file,dest_path)
            if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
                ROOT.gDirectory.Delete(obj.GetName()+";*")
            obj.Write()
            del obj

    chg_dir(dest_file,dest_path)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)
