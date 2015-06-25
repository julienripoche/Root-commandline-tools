#!/usr/bin/python

"""rfghfghfgh"""

from is_directory import *
from chg_dir import *
import ROOT

def dir_selector(root_file,path_list):
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

def get_key(root_file,path):
    chg_dir(root_file,path[:-1])
    return ROOT.gDirectory.GetKey(path[-1])

def get_key_list(root_file,path):
    chg_dir(root_file,path)
    return ROOT.gDirectory.GetListOfKeys()
