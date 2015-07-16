#!/usr/bin/python

"""Module which contain a function to copy objects from a root file to an other root file"""

from utils import *
import ROOT

def rooeventselector_select(source_file,source_path,dest_file,dest_path,opt_dict):
    """Create a copy of the oldtree selecting events"""

    chg_dir(source_file,source_path[:-1])
    oldtree = ROOT.gDirectory.Get(source_path[-1])
    nentries = oldtree.GetEntries()
    newtree = oldtree.CloneTree(0)
    
    if opt_dict["first"] != None: first_event = opt_dict["first"]
    else: first_event = 0
    if opt_dict["last"] != None: last_event = opt_dict["last"]
    else: last_event = nentries - 1

    for i in range(nentries):
        if i<500 and (i >= first_event and i <= last_event): # i<500 for debug
            #print str(i)+" ", for debug
            oldtree.GetEntry(i)
            newtree.Fill()

    chg_dir(dest_file,dest_path)
    newtree.Write()
