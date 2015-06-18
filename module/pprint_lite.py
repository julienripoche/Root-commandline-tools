#!/usr/bin/python

"""Module which contains a function to print list of strings in columns"""

# This code is adaptated from the pprint_list function here : http://stackoverflow.com/questions/25026556/output-list-like-ls
# Thanks hawkjo !!

import sys
from get_terminal_size import *
from initialize import * # bold and blue

def pprint_lite(repr_list):
    (term_width, term_height) =  get_terminal_size()
    #if len( str(repr_list) ) <= term_width:
    #    return
    min_chars_between = 2 # two spaces
    usable_term_width = term_width # - 3 # For '[ ' and ']' at beginning and end
    min_element_width = min( len(x) for x in repr_list ) + min_chars_between
    max_element_width = max( len(x) for x in repr_list ) + min_chars_between
    if max_element_width >= usable_term_width:
        ncol = 1
        col_widths = [1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(repr_list), usable_term_width / min_element_width  )
        while True:
            col_widths = [ max( len(x) + min_chars_between \
                                for j, x in enumerate( repr_list ) if j % ncol == i ) \
                                for i in range(ncol) ]
            if sum( col_widths ) <= usable_term_width: break
            else: ncol -= 1
    for i, x in enumerate(repr_list):
        sys.stdout.write(x.ljust(col_widths[i%ncol]))
        if i == len(repr_list) - 1 or (i+1) % ncol == 0:
            sys.stdout.write('\n')
