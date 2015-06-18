#!/usr/bin/python

"""Module which contains the File class"""

import ROOT

class File:
    """This class is used to easily manipulate the name, path
    and TFile of a root file"""

    def __init__(self,file_name,file_path=[]):
        """Constructor of File, needs the name of the root file,
        the path is optionnal"""
        self.name = file_name
        self.path = file_path
        self.root_file = ROOT.TFile()
        self.current_directory = self.root_file
        self.objects = []
        self.is_directory = True

    def open_tfile(self,access_mode=""):
        """Method to open the TFile which corresponds to the name,
        the access mode can be precised, reading mode by default"""
        self.root_file = self.root_file.Open(self.name,access_mode)
        self.current_directory = self.root_file

        ### Initialization of the is_directory boolean ### If we are in reading
        if access_mode=="" and self.path != []:
            self.change_directory(len(self.path)-1)
            if not "TDirectory" in self.current_directory.Get(self.path[len(self.path)-1]).IsA().GetName():
                self.is_directory = False
        self.change_directory(0)
        ### Initialization of the is_directory boolean ###

    def change_directory(self,localization):
        """Method to change the current directory by advancing in the path"""
        self.current_directory = self.root_file
        self.current_directory.cd()
        i = 0
        while i < localization:
            self.current_directory = self.current_directory.Get(self.path[i])
            self.current_directory.cd()
            i += 1

    def path_string(self):
        """Method which return the string path of an object in the root file"""
        return "/".join(self.path)

    def is_open(self):
        """Method to know if TFile is opened or not"""
        return self.root_file.IsOpen()

    def close_tfile(self):
        """Method to close the TFile"""
        if self.is_open():
            self.root_file.Close()
        else:
            print("Error : This TFile is already closed")

    def __del__(self):
        """Destructor method"""
        if self.is_open():
            self.root_file.Close()
