#!/usr/bin/python

"""Module which contain a function to give file/path
that matches which a pattern"""

import glob
import os
import fnmatch
from utils import *

def pattern_to_object(file_name,pattern):
    """Put in a list paths of objects in the root file
    corresponding to file_name that match with the pattern"""

    pattern_split = [n for n in pattern.split("/") if n != ""]

    # Full ROOT file, unnecessary but if not then opening of root_file unnecessary...
    if pattern_split == []:
        return [[]]

    root_file = ROOT.TFile.Open(file_name)
    path_list = [[]]
    for pattern_piece in pattern_split:
        new_path_list = []
        for path in path_list:
            chg_dir(root_file,path)
            for key in ROOT.gDirectory.GetListOfKeys():
                if fnmatch.fnmatch(key.GetName(),pattern_piece):
                    new_path = [n for n in path]
                    new_path.append(key.GetName())
                    new_path_list.append(new_path)
        path_list = new_path_list

    if path_list == []:
        print("pattern_to_object : can't find {0} in {1}".format(pattern,file_name))

    return path_list

def pattern_to_tuple(pattern,regexp = True):
    """Create a list of tuple which contain root file name
    and path list in this file of object that matches"""

    file_list = []
    pattern_split = pattern.split(":")
    if pattern_split[0] in ["http","https","ftp"]:
        # File from the web
        pattern_split[0] += ":"+pattern_split[1]
        del pattern_split[1]
        name_list = [pattern_split[0]]
    else:
        # Or not
        if regexp:
            name_list = [os.path.expandvars(os.path.expanduser(i)) \
                         for i in glob.iglob(pattern_split[0])]
        else:
            name_list = [os.path.expandvars(os.path.expanduser( \
                            pattern_split[0]))]

    for file_name in name_list:
        if len(pattern_split)==2:
            # There is a pattern of path in the ROOT file
            if regexp:
                path_list = pattern_to_object(file_name,pattern_split[1])
            else:
                path_list = [n for n in pattern_split[1].split("/") if n != ""]
        else:
            # This is the entire ROOT file
            path_list = [[]]
        file_list.append((file_name,path_list))

    return file_list
