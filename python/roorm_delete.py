#!/usr/bin/python

"""Module which contain a function to remove an object from a root file"""

from utils import *
import os
import ROOT

def roorm_delete(root_file,path):
    """Remove the object corresponding to the path from a root file"""
    if path != []:
        chg_dir(root_file,path[:-1])
        ROOT.gDirectory.Delete(path[-1]+";*")
        # It doesn't work without the +";*" for cycles
    else:
        os.system("rm {}".format(root_file.GetName()))
