#!/usr/bin/python

"""Module which contains a function to find path
of file that match with a pattern"""

import os
import fnmatch

def pattern_to_file(pattern):
    """Put in a list the names of files that match with the pattern"""

    # Treatment of the pattern to have something comparable to an absolute path
    pattern_norm = os.path.abspath(os.path.expanduser(os.path.normpath(pattern)))
    pattern_head,pattern_tail = os.path.split(pattern_norm)
    pattern_head_split = pattern_head.split("/")
    del pattern_head_split[0] # Because it's an absolute path (/etc/directory ...)

    # Search of the directory that is the lowest real directory on the hierarchy
    # This minimizes the calculations on the next loop using os.walk(path)
    lowest_real_dir = "/"
    for pattern_dir in pattern_head_split:
        dir_candidate = lowest_real_dir+pattern_dir+"/"
        if os.path.exists(dir_candidate):
            lowest_real_dir = dir_candidate
        else:
            break
    lowest_real_dir = os.path.normpath(lowest_real_dir)

    # Loop on all tuple (dir,dirname,filename) of the current directory which is lowest_real_dir
    # Add all file name that matches in file_name_list
    file_name_list = []
    for walk_tup in os.walk(lowest_real_dir):
        if fnmatch.fnmatch(walk_tup[0],pattern_head):
            for file_candidate in walk_tup[2]:
                if fnmatch.fnmatch(file_candidate,pattern_tail):
                    file_name_list.append(walk_tup[0]+"/"+file_candidate)

    if file_name_list == []:
        print("rools: cannot access {0}: No such file or directory".format(pattern))

    return file_name_list
