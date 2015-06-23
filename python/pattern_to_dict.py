#!/usr/bin/python

"""Create a dictionnary with ROOT file name as key
and which contains list of paths"""

from pattern_to_file import *
from pattern_to_object import *

def pattern_to_dict(pattern_list):
    """Create a dictionnary with ROOT file name as key and which
    contains list of paths"""

    file_dict = {}
    for pattern in pattern_list:
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
                path_list = []
            if not file_name in file_dict:
                file_dict[file_name] = path_list
            else:
                file_dict[file_name].extend(path_list)

    return file_dict

def pattern_to_dict_mkdir(pattern_list):
    """Create a dictionnary with ROOT file name as key and which
    contains list of paths"""

    file_dict = {}
    for pattern in pattern_list:
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
                # There is a pattern of path in the ROOT filen
                pattern = pattern_split[1]
                pattern_norm = os.path.normpath(pattern)
                pattern_split = pattern_norm.split("/")
                path_list = [pattern_split]
            else:
                # This is the entire ROOT file
                path_list = []
            if not file_name in file_dict:
                file_dict[file_name] = path_list
            else:
                file_dict[file_name].extend(path_list)

    return file_dict
