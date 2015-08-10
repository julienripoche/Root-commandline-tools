#!/usr/bin/python

"""Command line to dump ROOT files contents to terminal"""

from cmdLineUtils import *

ANSI_BOLD = "\x1B[1m"
ANSI_BLUE = "\x1B[34m"
ANSI_GREEN = "\x1B[32m"
ANSI_END = "\x1B[0m"

def colorInBold(string):
    """Color the string in bold if the output is the terminal"""
    if sys.stdout.isatty() \
       and sys.platform != 'win32': return ANSI_BOLD+string+ANSI_END
    else: return string

def colorInBlue(string):
    """Color the string in blue if the output is the terminal"""
    if sys.stdout.isatty() \
       and sys.platform != 'win32': return ANSI_BLUE+string+ANSI_END
    else: return string

def colorInGreen(string):
    """Color the string in green if the output is the terminal"""
    if sys.stdout.isatty() \
       and sys.platform != 'win32': return ANSI_GREEN+string+ANSI_END
    else: return string

TREE_TEMPLATE = "{0:{nameWidth}}"+"{1:{titleWidth}}{2:{memoryWidth}}"

def recursifTreePrinter(tree,indent):
    """Print recursively tree informations"""
    if len(tree.GetListOfBranches()) > 0: # Width informations
        maxCharName = max([len(branch.GetName()) \
            for branch in tree.GetListOfBranches()])
        maxCharTitle = max([len(branch.GetTitle()) \
            for branch in tree.GetListOfBranches()])
        dic = { \
            "nameWidth":maxCharName+2, \
            "titleWidth":maxCharTitle+4, \
            "memoryWidth":1}
    for branch in tree.GetListOfBranches(): # Print loop
        rec = \
            [branch.GetName(), \
            "\""+branch.GetTitle()+"\"", \
            str(branch.GetTotBytes())]
        print " "*indent + TREE_TEMPLATE.format(*rec,**dic)
        # if indentLevel < optDict["deeper_level"]: to keep in mind
        recursifTreePrinter(branch,indent+2)

def prepareTime(time):
    """Get time in the proper shape
    ex : 174512 for 17h 45m 12s
    ex : 094023 for 09h 40m 23s"""
    time = str(time)
    time = '000000'+time
    time = time[len(time)-6:]
    return time

MONTH = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun', \
         7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
LONG_TEMPLATE = \
    colorInBold("{0:{classWidth}}")+"{1:{timeWidth}}" + \
    "{2:{nameWidth}}{3:{titleWidth}}"

def roolsPrintLongLs(keyList,optDict,indent):
    """Print a list of Tkey in columns
    pattern : classname, datetime, name and title"""
    LONG_TEMPLATE_INDENTED = " "*indent + LONG_TEMPLATE
    if len(keyList) > 0: # Width informations
        maxCharClass = max([len(key.GetClassName()) for key in keyList])
        maxCharTime = 12
        maxCharName = max([len(key.GetName()) for key in keyList])
        dic = { \
            "classWidth":maxCharClass+2, \
            "timeWidth":maxCharTime+2, \
            "nameWidth":maxCharName+2, \
            "titleWidth":1}
    date = ROOT.Long(0)  
    for key in keyList:
        time = ROOT.Long(0)
        key.GetDatime().GetDateTime(key.GetDatime().Get(),date,time)
        time = prepareTime(time)
        rec = \
            [key.GetClassName(), \
            MONTH[int(str(date)[4:6])]+" " +str(date)[6:]+ \
            " "+time[:2]+":"+time[2:4], \
            key.GetName(), \
            "\""+key.GetTitle()+"\""]
        print LONG_TEMPLATE_INDENTED.format(*rec,**dic)
        if optDict['tree'] and isTreeKey(key):
            tree = key.ReadObj()
            recursifTreePrinter(tree,indent+2)

def write(string, indent=0):
    """Use sys.stdout.write to write the string
    with an indentation equal to indent"""
    sys.stdout.write(" "*indent + string)

def roolsPrintSimpleLs(keyList,indent):
    """Print list of strings in columns
    - blue for directories
    - green for trees"""
    # This code is adaptated from the pprint_list function here :
    # http://stackoverflow.com/questions/25026556/output-list-like-ls
    # Thanks hawkjo !!
    if len(keyList) == 0: return
    (term_width, term_height) = getTerminalSize()
    term_width = term_width - indent
    min_chars_between = 2
    min_element_width = min( len(key.GetName()) for key in keyList ) \
                        + min_chars_between
    max_element_width = max( len(key.GetName()) for key in keyList ) \
                        + min_chars_between
    if max_element_width >= term_width: ncol,col_widths = 1,[1]
    else:
        # Start with max possible number of columns and reduce until it fits
        ncol = min( len(keyList), term_width / min_element_width  )
        while True:
            col_widths = \
                [ max( len(key.GetName()) + min_chars_between \
                for j, key in enumerate(keyList) if j % ncol == i ) \
                for i in range(ncol) ]
            if sum( col_widths ) <= term_width: break
            else: ncol -= 1
    for i, key in enumerate(keyList):
        if i%ncol == 0: write("",indent) # indentation
        # Don't add spaces after the last element of the line or of the list
        if (i+1)%ncol != 0 and i != len(keyList)-1:
            if not sys.stdout.isatty(): write( \
                key.GetName().ljust(col_widths[i%ncol]))
            elif isDirectoryKey(keyList[i]): write( \
                colorInBlue(key.GetName()).ljust(col_widths[i%ncol] + 9))
                # len(ANSI_BLUE+ANSI_END) = len("\x1B[34m"+"\x1B[0m") = 9
            elif isTreeKey(keyList[i]): write( \
                colorInGreen(key.GetName()).ljust(col_widths[i%ncol] + 9))
                # len(ANSI_GREEN+ANSI_END) = len("\x1B[32m"+"\x1B[0m") = 9
            else: write(key.GetName().ljust(col_widths[i%ncol]))
        else: # No spaces after the last element of the line or of the list
            if not sys.stdout.isatty(): write(key.GetName())
            elif isDirectoryKey(keyList[i]): write(colorInBlue(key.GetName()))
            elif isTreeKey(keyList[i]): write(colorInGreen(key.GetName()))
            else: write(key.GetName())
            write('\n')

def roolsPrint(keyList,optDict,indent=0):
    """Print informations given by keyList with a rools
    style choosen with optDict"""
    if optDict['long'] or optDict['tree']: \
       roolsPrintLongLs(keyList,optDict,indent)
    else: roolsPrintSimpleLs(keyList,indent)

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=ROOLS_HELP)
parser.add_argument("sourcePatternList", help=SOURCES_HELP, nargs='+')
parser.add_argument("-l", "--long", help=LONG_PRINT_HELP, action="store_true")
parser.add_argument("-t", "--tree", help=TREE_PRINT_HELP, action="store_true")
args = parser.parse_args()

# Create a list of tuples that contain source ROOT file names
# and lists of path in these files
sourceList = \
    [tup for pattern in args.sourcePatternList \
    for tup in patternToFileNameAndPathSplitList(pattern)]

# Create a dictionnary with options
optDict = vars(args)
del optDict["sourcePatternList"]

# Initialize indent level
if len(sourceList) > 1: indent = 2
else : indent = 0

# Loop on the ROOT files
first_round_file = True
for fileName, pathSplitList in sourceList:
    with stderrRedirected():
        rootFile = ROOT.TFile.Open(fileName)
    objList,dirList = typeSelector(rootFile,pathSplitList)
    keyList = [getKey(rootFile,pathSplit) for pathSplit in objList]
    keyList.sort()
    dirList.sort()

    # Paths of file
    if len(sourceList) > 1: write("{0} :".format(fileName)+"\n")

    # Print with the rools style
    roolsPrint(keyList,optDict,indent)

    # Initialize indent directory level
    if len(pathSplitList) > 1: indentDir = 2
    else : indentDir = 0

    # Loop on the directories
    for pathSplit in dirList:
        keyList = getKeyList(rootFile,pathSplit)
        keyList.sort()

        # Paths of object
        if len(pathSplitList) > 1:
            write("{0} :".format("/".join(pathSplit))+"\n",indent)

        # Print with the rools style
        roolsPrint(keyList,optDict,indent+indentDir)

    rootFile.Close()