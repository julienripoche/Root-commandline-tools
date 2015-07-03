#!/usr/bin/python

"""Module which contain some usefull functions"""

import ROOT

def chg_dir(root_file,path):
    """Method to change the current directory with
     his path in a root file"""
    root_file.cd()
    for dir_name in path:
        ROOT.gDirectory.Get(dir_name).cd()

def is_directory(key):
    """Function to test if the object pointed by the key
    inherits from TDirectory"""
    # If function received (root_file,path)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return True
        else:
            key = get_key(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())

def get_key(root_file,path):
    """Give the TKey of the corresponding object"""
    chg_dir(root_file,path[:-1])
    return ROOT.gDirectory.GetKey(path[-1])

def get_key_list(root_file,path):
    """Give the list of TKey of the corresponding directory"""
    chg_dir(root_file,path)
    return ROOT.gDirectory.GetListOfKeys()

def dir_selector(root_file,path_list):
    """Separate directory and non directory object"""
    obj_list = []
    dir_list = []
    for path in path_list:
        if path != []:
            chg_dir(root_file,path[:-1])
            if is_directory(ROOT.gDirectory.GetKey(path[-1])):
                dir_list.append(path)
            else:
                obj_list.append(path)
        else:
            dir_list.append(path)
    return obj_list,dir_list
