#!/usr/bin/python

"""Module which contain a function to add directories in a root file"""

from utils import *
import ROOT

def create_dir(root_file,path):
    """Add a TDirectoryFile in a root file"""
    chg_dir(root_file,path[:-1])
    ROOT.gDirectory.mkdir(path[-1])

def roomkdir_mkdir(root_file,path,opt_dict):
    """Add directory in root file depending on options"""
    if not opt_dict["parents"]:
        # if path == [], an empty file is created
        if path != []:
            create_dir(root_file,path)
    else:
        for i in range(len(path)):
            current_path = path[:i+1]
            name_list = [key.GetName() for key in \
                         get_key_list(root_file,current_path[:-1])]
            if not current_path[-1] in name_list:
                create_dir(root_file,current_path)
