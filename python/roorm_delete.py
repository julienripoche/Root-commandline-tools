#!/usr/bin/python

"""Commandline to remove an object from a root file"""

from chg_dir import *
import os
import ROOT

def roorm_delete(root_file,path):
    if path != []:
        chg_dir(root_file,path[:-1])
        ROOT.gDirectory.Delete(path[-1]+";*")
        # It doesn't work without the +";*" for cycles
    else:
        os.system("rm {}".format(root_file.GetName()))
