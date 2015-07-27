#!/usr/bin/python

"""Contain help strings for ROOT commandlines tools"""

SOURCE_HELP = \
    "Path of the source(s), syntax :" + \
    "[filePath/]file[.root]:[objectPath/]object"
DEST_HELP = \
    "Path of the destination, syntax :" + \
    "[filePath/]file[.root]:[objectPath/]object"

ROOBROWSE_HELP = \
    "Open the ROOT file on a TBrowser"
ROOEVENTSELECTOR_HELP = \
    "Copy subsets of trees from source ROOT files" + \
    "to new trees on a destination ROOT file"
ROOCP_HELP = \
    "Copy objects from ROOT files into an other"
ROOLS_HELP = \
    "Dump ROOT files contents to terminal"
ROOMKDIR_HELP = \
    "Add directories in a ROOT files"
ROOMV_HELP = \
    "Move objects from ROOT files to an other"
ROOPRINT_HELP = \
    "Print ROOT files contents on ps,pdf or png,gif.. files"
ROORM_HELP = \
    "Remove objects from ROOT files"

COMPRESS_HELP = \
    "Change the compression settings of the destination file"
DIRECTORY_HELP = \
    "Put output files in a subdirectory named 'directory'"
EXTENSION_HELP = \
    "Specify output extension (ex: pdf, png)"
FIRST_EVENT_HELP = \
    "Specify the first event to copy"
FORCE_HELP = \
    "Force the removing"
LAST_EVENT_HELP = \
    "Specify the last event to copy"
LONG_PRINT_HELP = \
    "Use a long listing format" + \
    "LONG_TEMPLATE = class time name title"
MERGE_HELP = \
    "Merge files in a file named 'merge' (only for ps and pdf)"
PARENT_HELP = \
    "Make parent directories as needed, no error if existing"
RECREATE_HELP = \
    "Recreate the destination file"
TREE_PRINT_HELP = \
    "Print tree recursively and use a long listing format (-l option)" + \
    "TREE_TEMPLATE : name title totBytes"
