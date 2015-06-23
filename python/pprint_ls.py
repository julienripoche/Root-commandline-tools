#!/usr/bin/python

"""Module which contains a function to print list of strings in columns"""

# This code is adaptated from the pprint_list function here : http://stackoverflow.com/questions/25026556/output-list-like-ls
# Thanks hawkjo !!

import sys
from pretty_print import *
from utils.get_terminal_size import *

def pprint_ls(input_list):
    if len(input_list) == 0:
        return
    (term_width, term_height) =  get_terminal_size()
    min_chars_between = 2
    min_element_width = min( len(x) for x in input_list ) + min_chars_between
    max_element_width = max( len(x) for x in input_list ) + min_chars_between
    if max_element_width >= term_width:
        ncol = 1
        col_widths = [1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(input_list), term_width / min_element_width  )
        while True:
            col_widths = [ max( len(x) + min_chars_between \
                                for j, x in enumerate( input_list ) if j % ncol == i ) \
                                for i in range(ncol) ]
            if sum( col_widths ) <= term_width: break
            else: ncol -= 1
    for i, x in enumerate(input_list):
        sys.stdout.write(x.ljust(col_widths[i%ncol]))
        if i == len(input_list) - 1 or (i+1) % ncol == 0:
            sys.stdout.write('\n')
