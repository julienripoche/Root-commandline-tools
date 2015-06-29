#!/usr/bin/python

"""Module which contains a function to find path of
object in a file that match with a pattern"""

import os
import fnmatch
from chg_dir import *
from is_directory import *

def pattern_to_object(file_name,pattern):
    """Put in a list the paths that match with the pattern"""

    pattern_split = pattern.split("/")
    pattern_split = [n for n in pattern_split if n != ""]

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
        print("rools: cannot access {0}: No such file or directory".format(pattern))

    return path_list
