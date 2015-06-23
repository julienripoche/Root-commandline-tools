#!/usr/bin/python

"""Module which contains a function to change the current directory"""

import ROOT

def chg_dir(root_file,path):
    """Method to change the current directory with
     his path in a root file"""
    current_dir = root_file
    for dir_name in path:
        current_dir = current_dir.Get(dir_name)
    current_dir.cd()

#def chg_dir(root_file,path):
#    """Method to change the current directory with
#     his path in a root file"""
#    current_dir = root_file
#    for dir_name in path:
#        current_dir = current_dir.Get(dir_name)
#    current_dir.cd()
