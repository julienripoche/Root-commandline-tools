#!/usr/bin/python

"""dgfhdfgdfg"""

from pprint_long_ls import *
from pprint_ls import *
import ROOT

def rools_print(key_list,opt_dict):
    if opt_dict['l']:
        pprint_long_ls(key_list)
    else:
        # Don't forget color and bold, make a different function
        name_list = [key.GetName() for key in key_list]
        pprint_ls(name_list)
