#!/usr/bin/python

"""Module which contain a function to print key_list informations
with a rools style"""

from rools_utils.pprint_long_ls import *
from rools_utils.pprint_ls import *
import ROOT

def rools_print(key_list,opt_dict):
    """Print the informations given by key_list with a rools
    style choosen with opt_dict"""
    if opt_dict['l']:
        pprint_long_ls(key_list)
    else:
        # Don't forget color and bold, make a different function
        name_list = [key.GetName() for key in key_list]
        pprint_ls(name_list)
