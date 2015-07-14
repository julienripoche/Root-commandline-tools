#!/usr/bin/python

"""Module which contains a function to print a list of TKey properties in columns"""

import ROOT
from pretty_print import *
from utils import *

# Template for columns print
template = "{0:{name_width}}"+"{1:{title_width}}{2:{memory_width}}"

def recursif(tree,indentLevel):
    # Width informations
    if len(tree.GetListOfBranches()) > 0:
        max_name = max([len(branch.GetName()) for branch in tree.GetListOfBranches()])
        max_title = max([len(branch.GetTitle()) for branch in tree.GetListOfBranches()])
        #max_memory = max([len(str(branch.GetTotBytes())) for branch in tree.GetListOfBranches()])
        dic = {"name_width":max_name+2,"title_width":max_title+4,"memory_width":1}

    # Print loop
    for branch in tree.GetListOfBranches():
        # Data
        rec = [branch.GetName(), \
               "\""+branch.GetTitle()+"\"", \
               str(branch.GetTotBytes())]
        # Print
        print "  "*indentLevel + template.format(*rec,**dic)
        recursif(branch,indentLevel+1)

def pprint_tree_ls(key_list):
    """Function to print contents of trees"""
    for key in key_list:
        if is_tree(key):
            tree = key.ReadObj()
            rec = [tree.GetName(), \
               "\""+tree.GetTitle()+"\"", \
               str(tree.GetTotBytes())]
            dic = {"name_width":len(tree.GetName())+2,"title_width":len(tree.GetTitle())+4,"memory_width":1}
            print template.format(*rec,**dic)
            recursif(tree,1)
