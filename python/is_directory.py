#!/usr/bin/python

"""Module which contain a test of TDirectory"""

import ROOT

def is_directory(key):
    """Function to test if the object pointed by the key
    inherits from TDirectory"""
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    if (cl.InheritsFrom(ROOT.TDirectory.Class())):
        return True
    else:
        return False
