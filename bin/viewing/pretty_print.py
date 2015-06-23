#!/usr/bin/python

"""Module which contains some pretty print functions"""

def ansi_bold(string):
    """Make the string bold"""
    ansi_bold = "\x1B[1m"
    ansi_end = "\x1B[0m"
    return ansi_bold+string+ansi_end

def ansi_blue(string):
    """Make the string blue"""
    ansi_blue = "\x1B[34m"
    ansi_end = "\x1B[0m"
    return ansi_blue+string+ansi_end
