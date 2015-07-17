#!/usr/bin/python

"""Test module for pattern to tuple"""

from redirect_escape_characters import *

with stdout_redirected(to=os.devnull), merged_stderr_stdout():
    from cmdLineUtils import pattern_to_tuple
    import argparse

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description="test for pattern to tuple function")
parser.add_argument("pattern_list", \
                    help="file path and object path in the file with the syntax : [file_path/]file[.root]:[object_path/]object", \
                    nargs='+')
args = parser.parse_args()

# Create a list of tuples that contain a ROOT file name and a list of path in this file
file_list = []
for pattern in args.pattern_list:
    file_list.extend(pattern_to_tuple(pattern))

print file_list
