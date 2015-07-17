#!/usr/bin/python

"""Contain all utils for ROOT commandlines tools"""

# Redirection of escape characters during importations
from redirect_escape_characters import *
with stdout_redirected(to=os.devnull), merged_stderr_stdout():
    from get_terminal_size import *
    import ROOT
    import argparse
    import glob
    import os
    import sys
    import fnmatch

def chg_dir(root_file,path):
    """Change the current directory for
    (root_file,path) in root_file"""
    root_file.cd()
    for dir_name in path:
        ROOT.gDirectory.Get(dir_name).cd()

def get_key(root_file,path):
    """Give the key of the corresponding object"""
    chg_dir(root_file,path[:-1])
    return ROOT.gDirectory.GetKey(path[-1])

def is_directory(key):
    """Test if the object pointed by the key
    inherits from TDirectory"""
    # If function received (root_file,path)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return True
        else:
            key = get_key(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TDirectory.Class())

def is_tree(key):
    """Test if the object pointed by the key
    inherits from TTree"""
    # If function received (root_file,path)
    if type(key) != ROOT.TKey:
        if key[1] == []:
            return False
        else:
            key = get_key(key[0],key[1])
    classname = key.GetClassName()
    cl = ROOT.gROOT.GetClass(classname)
    return cl.InheritsFrom(ROOT.TTree.Class())

def get_key_list(root_file,path):
    """Give the list of key of the corresponding directory,
    if (root_file,path) is not a directory give corresponding key"""
    if is_directory((root_file,path)):
        chg_dir(root_file,path)
        return ROOT.gDirectory.GetListOfKeys()
    else:
        return [get_key(root_file,path)]

def type_selector(root_file,path_list):
    """Separate directories, branches and other objects"""
    obj_list = []
    dir_list = []
    #branch_list = []
    for path in path_list:
        if path == []:
            dir_list.append(path)
        elif is_tree((root_file,path[:-1])):
            pass
            #branch_list.append(path)
        elif is_directory((root_file,path)):
            dir_list.append(path)
        else:
            obj_list.append(path)
    return obj_list,dir_list#,branch_list

def pattern_to_object(file_name,pattern):
    """Put in a list path of objects in the ROOT file
    corresponding to file_name that match with the pattern"""
    pattern_split = [n for n in pattern.split("/") if n != ""]
    # Full ROOT file, unnecessary but if not
    # then opening of root_file for nothing...
    if pattern_split == []:
        return [[]]
    root_file = ROOT.TFile.Open(file_name)
    path_list = [[]]
    for pattern_piece in pattern_split:
        new_path_list = []
        for path in path_list:
            if is_tree((root_file,path[:-1])):
                # Security to stay in top level of trees
                continue
            elif is_directory((root_file,path)):
                chg_dir(root_file,path)
                new_path_list.extend([path + [key.GetName()]\
                                      for key in ROOT.gDirectory.GetListOfKeys()\
                                      if fnmatch.fnmatch(key.GetName(),pattern_piece)])
            elif is_tree((root_file,path)):
                chg_dir(root_file,path[:-1])
                T = ROOT.gDirectory.Get(path[-1])
                new_path_list.extend([path + [branch.GetName()]\
                                      for branch in T.GetListOfBranches()\
                                      if fnmatch.fnmatch(branch.GetName(),pattern_piece)])
        path_list = new_path_list
    if path_list == []:
        print("pattern_to_object : can't find {0} in {1}".format(pattern,file_name))
    return path_list

def pattern_to_tuple(pattern,regexp = True):
    """Create a list of tuple which contain root file name
    and path list in this file of object that matches"""
    file_list = []
    pattern_split = pattern.split(":")
    if pattern_split[0] in ["http","https","ftp"]:
        # File from the web
        pattern_split[0] += ":"+pattern_split[1]
        del pattern_split[1]
        name_list = [pattern_split[0]]
    else:
        if regexp:
            name_list = [os.path.expandvars(os.path.expanduser(i)) \
                         for i in glob.iglob(pattern_split[0])]
        else:
            name_list = [os.path.expandvars(os.path.expanduser( \
                            pattern_split[0]))]
    for file_name in name_list:
        if len(pattern_split)==2:
            # There is a pattern of path in the ROOT file
            if regexp:
                path_list = pattern_to_object(file_name,pattern_split[1])
            else:
                path_list = [[n for n in pattern_split[1].split("/") if n != ""]]
        else:
            # This is the entire ROOT file
            path_list = [[]]
        file_list.append((file_name,path_list))
    return file_list

def copier(source_file,source_path,dest_file,dest_path):
    """Python adaptation of a root input/output tutorial :
    $ROOTSYS/tutorials/io/copyFiles.C"""
    for key in get_key_list(source_file,source_path):
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if (not cl):
            return
        if (cl.InheritsFrom(ROOT.TDirectory.Class())):
            chg_dir(dest_file,dest_path)
            if not ROOT.gDirectory.GetListOfKeys().Contains(key.GetName()):
                ROOT.gDirectory.mkdir(key.GetName())
            chg_dir(source_file,source_path+[key.GetName()])
            copier(source_file,source_path+[key.GetName()],dest_file,dest_path+[key.GetName()])
        elif (cl.InheritsFrom(ROOT.TTree.Class())):
            chg_dir(source_file,source_path[:-1])
            print "problem with cycles, don't forget to look at it..."
            T = ROOT.gDirectory.Get(key.GetName()+";1")
            chg_dir(dest_file,dest_path)
            newT = T.CloneTree(-1,"fast")
            newT.Write()
        else:
            obj = key.ReadObj()
            chg_dir(dest_file,dest_path)
            if ROOT.gDirectory.GetListOfKeys().Contains(obj.GetName()):
                ROOT.gDirectory.Delete(obj.GetName()+";*")
            obj.Write()
            del obj

    chg_dir(dest_file,dest_path)
    ROOT.gDirectory.SaveSelf(ROOT.kTRUE)

def deleter(root_file,path,opt_dict):
    """Remove the object corresponding to the path
    from a ROOT file, option force to avoid the confirmation"""
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
