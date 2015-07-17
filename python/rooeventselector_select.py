#!/usr/bin/python

"""Module which contain a function to copy objects from a root file to an other root file"""

from utils import *
import ROOT

def rooeventselector_select(source_file,source_path,dest_file,dest_path,opt_dict):
    """Create a copy of the oldtree selecting events"""

    chg_dir(source_file,source_path[:-1])
    bigtree = ROOT.gDirectory.Get(source_path[-1])
    nentries = bigtree.GetEntries()
    chg_dir(dest_file,dest_path) # For the small tree not to be memory resident
    smalltree = bigtree.CloneTree(0)
    
    if opt_dict["first"] != None:
        first_event = opt_dict["first"]
    else:
        first_event = 0
    if opt_dict["last"] != None:
        last_event = opt_dict["last"]
    else:
        last_event = nentries - 1
            
    for i in range(nentries):
        if i >= first_event and i <= last_event:
            bigtree.GetEntry(i)
            smalltree.Fill()
                
    chg_dir(dest_file,dest_path)
    smalltree.Write()
