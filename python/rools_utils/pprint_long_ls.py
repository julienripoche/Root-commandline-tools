#!/usr/bin/python

"""Module which contains a function to print a list of TKey properties in columns"""

import ROOT
from pretty_print import *

def time_preparator(time):
    """ Function to be sure of the format of time
    (174512 for 17h 45m 12s and 094023 for 09h 40m 23s)"""
    time = str(time)
    time = '000000'+time
    time = time[len(time)-6:]
    return time

def pprint_long_ls(key_list):
    """Function to print a list of Tkey in columns,
    classname, datetime, name and title"""

    # Template for columns print
    template = ansi_bold("{0:{class_width}}")+"{1:{time_width}}{2:{name_width}}{3:{title_width}}"

    # Width informations
    if len(key_list) > 0:
        max_class = max([len(key.GetClassName()) for key in key_list])
        max_time = 12
        max_name = max([len(key.GetName()) for key in key_list])
        #max_title = max([len(key.GetTitle()) for key in key_list])
        dic = {"class_width":max_class+2,"time_width":max_time+2,"name_width":max_name+2,"title_width":1}

    date =ROOT.Long(0)  
    month={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    for key in key_list:
        time =ROOT.Long(0)
        key.GetDatime().GetDateTime(key.GetDatime().Get(),date,time)
        time = time_preparator(time)
        rec = [key.GetClassName(), \
               month[int(str(date)[4:6])]+" " +str(date)[6:]+" "+time[:2]+":"+time[2:4], \
               key.GetName(), \
               "\""+key.GetTitle()+"\""]
        print template.format(*rec,**dic)
