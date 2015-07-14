#!/usr/bin/python

"""Module which contain some usefull functions"""

import ROOT

def chg_dir(root_file,path):
    """Method to change the current directory
    for one in a root file"""
    root_file.cd()
    for dir_name in path:
        ROOT.gDirectory.Get(dir_name).cd()

def get_key(root_file,path):
    """Give the TKey of the corresponding object"""
    chg_dir(root_file,path[:-1])
    return ROOT.gDirectory.GetKey(path[-1])

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

def is_tree(key):
    """Function to test if the object pointed by the key
    inherits from TTree"""
    # If function received (root_file,path)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return False
        else:
            key = get_key(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())

def get_key_list(root_file,path):
    """Give the list of TKey of the corresponding directory"""
    if is_directory((root_file,path)):
        chg_dir(root_file,path)
        return ROOT.gDirectory.GetListOfKeys()
    else:
        return [get_key(root_file,path)]

def type_selector(root_file,path_list):
    """Separate directories, branches and other objects"""
    obj_list = []
    dir_list = []
    #branch_list = []
    for path in path_list:
        if path == []:
            dir_list.append(path)
        elif is_tree((root_file,path[:-1])):
            pass
            #branch_list.append(path)
        elif is_directory((root_file,path)):
            dir_list.append(path)
        else:
            obj_list.append(path)
    return obj_list,dir_list#,branch_list
