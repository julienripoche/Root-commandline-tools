#!/usr/bin/python

"""Module which contains a function to print a list of TKey in columns"""

import ROOT
from pretty_print import *

def pprint_long(key_list):
    """Function to print a list of Tkey in columns,
    classname, datetime, name and title"""

    # Template for columns print
    template = ansi_bold("{0:{class_width}}")+"{1:{time_width}}{2:{name_width}}{3:{title_width}}"

    date =ROOT.Long(0)
    time =ROOT.Long(0)    
    month={1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
    
    data_source = []
    for key in key_list:
        key.GetDatime().GetDateTime(key.GetDatime().Get(),date,time)
        data_source.append([key.GetClassName(), \
                            month[int(str(date)[4:6])]+" " +str(date)[6:]+" "+str(time)[:2]+":"+str(time)[2:4], \
                            key.GetName(), \
                            "\""+key.GetTitle()+"\""])

    # Width information
    max_class = max([len(key.GetClassName()) for key in key_list])
    max_time = 12
    max_name = max([len(key.GetName()) for key in key_list])
    max_title = max([len(key.GetTitle()) for key in key_list])
    dic = {"class_width":max_class+2,"time_width":max_time+2,"name_width":max_name+2,"title_width":max_title}

    # Loop
    for rec in data_source: 
        print template.format(*rec,**dic)
