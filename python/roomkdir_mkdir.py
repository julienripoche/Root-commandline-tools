#!/usr/bin/python

"""Module which contain a function to add a directory in a root file"""

from utils import *
import ROOT

def roomkdir_mkdir(root_file,path):
    """Add a TDirectoryFile in a root file"""
    # if path == [], an empty file is created
    if path != []:
        chg_dir(root_file,path[:-1])
        ROOT.gDirectory.mkdir(path[-1])
