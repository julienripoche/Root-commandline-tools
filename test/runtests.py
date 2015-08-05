#!/usr/bin/python

import os
import shutil
import sys

if sys.platform == 'win32':
    os.environ["PATHEXT"] += os.pathsep + ".py"

failure_nb = 0
test_nb = 0

def cmp_lines(path_1, path_2):
    l1 = l2 = ' '
    with open(path_1, 'U') as f1:
        with open(path_2, 'U') as f2:
            while l1 != '' and l2 != '':
                l1 = f1.readline()
                l2 = f2.readline()
                if l1 != l2:
                    return False
    return True

def testCommand(testName,command,refFileName):
    ofileName = testName+".out"
    command += " > %s 2>&1" %ofileName
    os.system(command)
    print "Test %s" %testName,
    global test_nb
    test_nb += 1
    if cmp_lines(ofileName,refFileName):
        print "SUCCESS"
    else:
        print "FAILURE"
        global failure_nb
        failure_nb += 1

############################## PATTERN TESTS ############################
testCommand("SimplePattern", "python testPatternToFileNameAndPathSplitList.py test.root", "SimplePattern.ref")
testCommand("SimplePattern2", "python testPatternToFileNameAndPathSplitList.py test.root:tof", "SimplePattern2.ref")
testCommand("SimplePattern3", "python testPatternToFileNameAndPathSplitList.py test.root:*", "SimplePattern3.ref")
#########################################################################

############################## ROOLS TESTS ##############################
testCommand("SimpleRools", "rools test.root", "SimpleRools.ref")
testCommand("SimpleRools2", "rools test.root:*", "SimpleRools2.ref")
testCommand("SimpleRools3", "rools test.root:tof", "SimpleRools3.ref")
testCommand("SimpleRools4", "rools test.root:tof/*", "SimpleRools4.ref")
testCommand("LongRools", "rools -l test.root", "LongRools.ref")
testCommand("LongRools2", "rools -l test.root:*", "LongRools2.ref")
testCommand("LongRools3", "rools -l test.root:tof", "LongRools3.ref")
testCommand("LongRools4", "rools -l test.root:tof/*", "LongRools4.ref")
testCommand("WebRools", "rools http://root.cern.ch/files/pippa.root", "WebRools.ref")
testCommand("WebRools2", "rools -l http://root.cern.ch/files/pippa.root", "WebRools2.ref")
#########################################################################

############################## ROOCP TESTS ##############################
shutil.copy("test.root","source.root")
os.system("roocp source.root dest.root")
testCommand("SimpleRoocp", "rools dest.root", "SimpleRools.ref")
testCommand("SimpleRoocp2", "rools dest.root:*", "SimpleRools2.ref")
testCommand("SimpleRoocp3", "rools dest.root:tof", "SimpleRools3.ref")
testCommand("SimpleRoocp4", "rools dest.root:tof/*", "SimpleRools4.ref")
print "Test SimpleRoocp5",
test_nb += 1
if os.path.isfile("source.root") and os.path.isfile("dest.root"):
    print "SUCCESS"
    os.remove("source.root")
    os.remove("dest.root")
else:
    print "FAILURE"
    failure_nb += 1
    if os.path.isfile("source.root"):
        os.remove("source.root")
    if os.path.isfile("dest.root"):
        os.remove("dest.root")
#########################################################################

############################## ROOMV TESTS ##############################
shutil.copy("test.root","source.root")
os.system("roomv source.root dest.root")
testCommand("SimpleRoomv", "rools dest.root", "SimpleRools.ref")
testCommand("SimpleRoomv2", "rools dest.root:*", "SimpleRools2.ref")
testCommand("SimpleRoomv3", "rools dest.root:tof", "SimpleRools3.ref")
testCommand("SimpleRoomv4", "rools dest.root:tof/*", "SimpleRools4.ref")
print "Test SimpleRoomv5",
test_nb += 1
if not os.path.isfile("source.root") and os.path.isfile("dest.root"):
    print "SUCCESS"
    os.remove("dest.root")
else:
    print "FAILURE"
    failure_nb += 1
    if os.path.isfile("source.root"):
        os.remove("source.root")
    if os.path.isfile("dest.root"):
        os.remove("dest.root")
#########################################################################

############################## ROORM TESTS ##############################
shutil.copy("test.root","victim.root")
testCommand("SimpleRoorm", "roorm victim.root:hpx && rools victim.root", "SimpleRoorm.ref")
if os.path.isfile("victim.root"):
    os.remove("victim.root")
shutil.copy("test.root","victim.root")
testCommand("SimpleRoorm2", "roorm victim.root:tof/plane0 && rools victim.root:tof", "SimpleRoorm2.ref")
if os.path.isfile("victim.root"):
    os.remove("victim.root")
print "Test SimpleRoorm3",
test_nb += 1
shutil.copy("test.root","victim.root")
os.system("roorm victim.root")
if not os.path.isfile("victim.root"):
    print "SUCCESS"
else:
    print "FAILURE"
    failure_nb += 1
    os.remove("victim.root")
#########################################################################

############################# ROOMKDIR TESTS ############################
shutil.copy("test.root","target.root")
testCommand("SimpleRoomkdir", "roomkdir target.root:new_directory && rools target.root", "SimpleRoomkdir.ref")
if os.path.isfile("target.root"):
    os.remove("target.root")
shutil.copy("test.root","target.root")
testCommand("SimpleRoomkdir2", "roomkdir target.root:dir/new_directory && rools target.root:dir", "SimpleRoomkdir2.ref")
if os.path.isfile("target.root"):
    os.remove("target.root")
testCommand("SimpleRoomkdir3", "roomkdir target.root && rools target.root", "SimpleRoomkdir3.ref")
if os.path.isfile("target.root"):
    os.remove("target.root")
shutil.copy("test.root","target.root")
testCommand("SimpleRoomkdir4", "roomkdir -p target.root:a/b/c && rools target.root:a/b", "SimpleRoomkdir4.ref")
if os.path.isfile("target.root"):
    os.remove("target.root")
#########################################################################

################################ THE END ################################
print("\nResults :")
print("{0} failure(s) on {1} test(s)".format(failure_nb,test_nb))
#########################################################################
