#!/usr/bin/python

"""Commandline to add a directory in a root file"""

from chg_dir import *
import ROOT

def roomkdir_mkdir(root_file,path):
    if path != []:
        chg_dir(root_file,path[:-1])
        ROOT.gDirectory.mkdir(path[-1])
    else:
        print("Error : you can't create a directory without name it")