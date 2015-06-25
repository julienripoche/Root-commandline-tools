#!/usr/bin/python

"""Commandline to remove an object from a root file"""

from chg_dir import *
import ROOT

def roorm_delete(root_file,path):
    if path != []:
        chg_dir(root_file,path[:-1])
        ROOT.gDirectory.Delete(path[-1]+";*")
        # It doesn't work without the +";*" for cycles
    else:
        print("You want to delete a entire file, it's not currently possible")
