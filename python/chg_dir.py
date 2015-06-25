#!/usr/bin/python

"""Module which contains a function to change the current directory"""

import ROOT

def chg_dir(root_file,path):
    """Method to change the current directory with
     his path in a root file"""
    root_file.cd()
    for dir_name in path:
        ROOT.gDirectory.Get(dir_name).cd()
