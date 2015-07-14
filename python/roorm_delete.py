#!/usr/bin/python

"""Module which contain a function to remove an object from a root file"""

from utils import *
import os
import ROOT

def roorm_delete(root_file,path,opt_dict):
    """Remove the object corresponding to the path from a root file
    depending on options"""
    do_remove = True
    if not opt_dict['force']:
        if path != []:
            answer = raw_input("Are you sure to remove '{0}' from '{1}' ? (y/n) : " \
                                   .format("/".join(path),root_file.GetName()))
        else:
            answer = raw_input("Are you sure to remove '{0}' ? (y/n) : " \
                                   .format(root_file.GetName()))
        if answer.lower() != 'y':
            do_remove = False
    if do_remove:
        if path != []:
            chg_dir(root_file,path[:-1])
            ROOT.gDirectory.Delete(path[-1]+";*")
        else:
            os.system("rm {}".format(root_file.GetName()))
