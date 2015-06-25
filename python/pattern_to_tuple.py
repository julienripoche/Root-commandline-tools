#!/usr/bin/python

"""Create a dictionnary with ROOT file name as key
and which contains list of paths"""

from pattern_to_file import *
from pattern_to_object import *

def pattern_to_tuple(pattern):
    """Create a dictionnary with ROOT file name as key and which
    contains list of paths"""

    file_list = []
    pattern_split = pattern.split(":")
    if pattern_split[0] in ["http","https","ftp"]:
        # File from the web
        pattern_split[0] += ":"+pattern_split[1]
        del pattern_split[1]
        name_list = [pattern_split[0]]
    else:
        # Or not
        name_list = pattern_to_file(pattern_split[0])
    for file_name in name_list:
        if len(pattern_split)==2:
            # There is a pattern of path in the ROOT file
            path_list = pattern_to_object(file_name,pattern_split[1])
        else:
            # This is the entire ROOT file
            path_list = [[]]
        file_list.append((file_name,path_list))

    return file_list

def pattern_to_tuple_mkdir(pattern):
    """Create a dictionnary with ROOT file name as key and which
    contains list of paths"""

    pattern_split = pattern.split(":")
    if pattern_split[0] in ["http","https","ftp"]:
        # File from the web
        pattern_split[0] += ":"+pattern_split[1]
        del pattern_split[1]
        file_name = pattern_split[0]
    else:
        # Or not
        file_name = os.path.abspath(os.path.expanduser(os.path.normpath(pattern_split[0])))
    if len(pattern_split)==2:
        # There is a pattern of path in the ROOT file
        path_list = [os.path.normpath(pattern_split[1]).split("/")]
    else:
        # This is the entire ROOT file
        path_list = [[]]

    return (file_name,path_list)
