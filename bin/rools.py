#!/usr/bin/python

"""Command line to dump ROOT files contents to terminal"""

from cmdLineUtils import *

ANSI_BOLD = "\x1B[1m"
ANSI_BLUE = "\x1B[34m"
ANSI_GREEN = "\x1B[32m"
ANSI_END = "\x1B[0m"

def isTerminal():
    """Return True if the output is a terminal"""
    return sys.stdout.isatty()

def isWin32():
    """Return True if the platform is Windows"""
    return sys.platform == 'win32'

def isSpecial(ansiCode,string):
    """Use ansi code on 'string' if the output is the
    terminal of a not Windows platform"""
    if isTerminal() and not isWin32(): return ansiCode+string+ANSI_END
    else: return string

def write(string,indent=0,end=""):
    """Use sys.stdout.write to write the string with an indentation
    equal to indent and specifying the end character"""
    sys.stdout.write(" "*indent+string+end)

TREE_TEMPLATE = "{0:{nameWidth}}"+"{1:{titleWidth}}{2:{memoryWidth}}"

def recursifTreePrinter(tree,indent):
    """Print recursively tree informations"""
    listOfBranches = tree.GetListOfBranches()
    if len(listOfBranches) > 0: # Width informations
        maxCharName = max([len(branch.GetName()) \
            for branch in listOfBranches])
        maxCharTitle = max([len(branch.GetTitle()) \
            for branch in listOfBranches])
        dic = { \
            "nameWidth":maxCharName+2, \
            "titleWidth":maxCharTitle+4, \
            "memoryWidth":1}
    for branch in listOfBranches: # Print loop
        rec = \
            [branch.GetName(), \
            "\""+branch.GetTitle()+"\"", \
            str(branch.GetTotBytes())]
        write(TREE_TEMPLATE.format(*rec,**dic),indent,end="\n")
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
    isSpecial(ANSI_BOLD,"{0:{classWidth}}")+"{1:{timeWidth}}" + \
    "{2:{nameWidth}}{3:{titleWidth}}"

def roolsPrintLongLs(keyList,optDict,indent):
    """Print a list of Tkey in columns
    pattern : classname, datetime, name and title"""
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
        write(LONG_TEMPLATE.format(*rec,**dic),indent,end="\n")
        if optDict['tree'] and isTreeKey(key):
            tree = key.ReadObj()
            recursifTreePrinter(tree,indent+2)

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
            if not isTerminal(): write( \
                key.GetName().ljust(col_widths[i%ncol]))
            elif isDirectoryKey(keyList[i]): write( \
                isSpecial(ANSI_BLUE,key.GetName()).ljust(col_widths[i%ncol] + 9))
                # len(ANSI_BLUE+ANSI_END) = len("\x1B[34m"+"\x1B[0m") = 9
            elif isTreeKey(keyList[i]): write( \
                isSpecial(ANSI_GREEN,key.GetName()).ljust(col_widths[i%ncol] + 9))
                # len(ANSI_GREEN+ANSI_END) = len("\x1B[32m"+"\x1B[0m") = 9
            else: write(key.GetName().ljust(col_widths[i%ncol]))
        else: # No spaces after the last element of the line or of the list
            if not isTerminal(): write(key.GetName())
            elif isDirectoryKey(keyList[i]): write(isSpecial(ANSI_BLUE,key.GetName()))
            elif isTreeKey(keyList[i]): write(isSpecial(ANSI_GREEN,key.GetName()))
            else: write(key.GetName())
            write('\n')

def roolsPrint(keyList,optDict,indent=0):
    """Print informations given by keyList with a rools
    style choosen with optDict"""
    if optDict['long'] or optDict['tree']: \
       roolsPrintLongLs(keyList,optDict,indent)
    else: roolsPrintSimpleLs(keyList,indent)

#Help strings

COMMAND_HELP = \
    "Display ROOT files contents in the terminal " + \
    "(for more informations please look at the man page)."
LONG_PRINT_HELP = \
    "use a long listing format."
TREE_PRINT_HELP = \
    "print tree recursively and use a long listing format."

##### Beginning of the main code #####

# Collect arguments with the module argparse
parser = argparse.ArgumentParser(description=COMMAND_HELP)
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

# Initialize a boolean and indent level
manySources = len(sourceList) > 1
indent = 2 if manySources else 0

# Loop on the ROOT files
first_round_file = True
for fileName, pathSplitList in sourceList:
    with stderrRedirected():
        rootFile = ROOT.TFile.Open(fileName)
    objList,dirList = keyClassSpliter(rootFile,pathSplitList)
    keyList = [getKey(rootFile,pathSplit) for pathSplit in objList]
    keyList.sort()
    dirList.sort()

    # Paths of file
    if manySources: write("{0} :".format(fileName)+"\n")

    # Print with the rools style
    roolsPrint(keyList,optDict,indent)

    # Initialize a boolean and indent directory level
    manyPathSplits = len(pathSplitList) > 1
    indentDir = 2 if manyPathSplits else 0

    # Loop on the directories
    for pathSplit in dirList:
        keyList = getKeyList(rootFile,pathSplit)
        keyList.sort()

        # Paths of object
        if manyPathSplits:
            write("{0} :".format("/".join(pathSplit)),indent,end="\n")

        # Print with the rools style
        roolsPrint(keyList,optDict,indent+indentDir)

    rootFile.Close()
