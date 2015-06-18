#!/usr/bin/python

"""Module which contains an initializing function"""

from File import *
import fnmatch
import argparse
import os

def pattern_to_file(path):
    """Put in a list all files which match with the pattern"""

    path = path.split('/')
    location_list=['.']
    new_location_list=[]
    for pattern in path:
        for location in location_list:
            for file_name in os.listdir(location):
                if fnmatch.fnmatch(file_name,pattern):
                    new_location_list.append(location+'/'+file_name)
        location_list = new_location_list
        new_location_list=[]
    return location_list

def pattern_to_object(file_name,path,command_name):
    """Put in a list all files which match with the pattern \
    depending on the command which is being used"""

    if command_name == "ls" or command_name == "rm" or command_name == "cp":
        root_File = File(file_name)
        location_list = [root_File]
        new_location_list=[]
        i=0
        first = True
        for pattern in path:
            for location in location_list:
                location.open_tfile()
                location.change_directory(len(location.path))
                for key in location.current_directory.GetListOfKeys():
                    if fnmatch.fnmatch(key.GetName(),pattern):
                        new_list = [n for n in location.path]
                        new_list.append(key.GetName())

                        if command_name == "ls":
                            if i == len(path)-1: # Last step in the loop
                                root_File = File(file_name,new_list)
                                root_File.open_tfile()
                                if root_File.is_directory:
                                    new_location_list.append(File(file_name,new_list))
                                else:
                                    if first:
                                        container = root_File
                                        first = False
                                    container.objects.append(key.GetName())
                                root_File.close_tfile()
                            else:
                                new_location_list.append(File(file_name,new_list))
                        if command_name == "rm" or command_name == "cp":
                            new_location_list.append(File(file_name,new_list))
                location.close_tfile()
                if command_name == "ls":
                    if first == False:
                        del container.path[len(container.path)-1]
                        new_location_list.append(container)
                        first = True
            location_list = new_location_list
            new_location_list = []
        i += 1
        return location_list
    if command_name == "mkdir":
        return [File(file_name,path)]

def initialize(command_name):
    """Initializing function which returns a list of File and options"""

    # Use the argparse module to have informations about arguments and options
    if command_name == "ls":
        parser = argparse.ArgumentParser(description="commandline to print some informations about the contents of a root file")
        parser.add_argument("-l", help="use a long listing format", action="store_true")
    if command_name == "rm":
        parser = argparse.ArgumentParser(description="commandline to remove an object from a root file")
        parser.add_argument("-f", help="force the removing", action="store_true")
    if command_name == "cp":
        parser = argparse.ArgumentParser(description="commandline to cp an object from a root file to an other")
    if command_name == "mkdir":
        parser = argparse.ArgumentParser(description="commandline to add a directory in a root file")
    parser.add_argument("file_path_list", help="file path and object path in the file with the syntax : [file_path/]file[.root]:[object_path/]object", nargs='+')
    args = parser.parse_args()

    # Create a File list with file_path_list
    File_list = []
    i = 0
    for string in args.file_path_list:
        if i < len(args.file_path_list)-1 or not command_name == "cp":
            string_split = string.split(":")
            name_list = pattern_to_file(string_split[0])
            for file_name in name_list:
                if os.path.exists(file_name):
                    if len(string_split)==2: # Split the path if there is a "/"
                        file_path = string_split[1].split("/")
                    else:
                        file_path = []
                    File_list.extend(pattern_to_object(file_name,file_path,command_name))
                else:
                    print("root-"+command_name+": cannot access {}: No such file".format(file_name))
        else:
            File_list.append(File(file_name,file_path))
            

    # Create a dictionnary with options
    opt_dict = vars(args)
    del opt_dict["file_path_list"]

    # Return files informations and options
    return File_list,opt_dict
