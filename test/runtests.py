#! /usr/bin/env python

import os
import filecmp

failure_nb = 0
test_nb = 0

def testCommand(testName,command,refFileName):
    ofileName = testName+".out"
    command += " >& %s" %ofileName
    os.system(command)
    print "Test %s" %testName,
    global test_nb
    test_nb += 1
    if filecmp.cmp(ofileName,refFileName):
        print "SUCCESS"
    else:
        print "FAILURE"
        global failure_nb
        failure_nb += 1


############################## PATTERN TESTS ############################
testCommand("SimplePattern", "./test_pattern_to_tuple.py test.root", "SimplePattern.ref")
testCommand("SimplePattern2", "./test_pattern_to_tuple.py test.root:tof", "SimplePattern2.ref")
testCommand("SimplePattern3", "./test_pattern_to_tuple.py test.root:*", "SimplePattern3.ref")
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
testCommand("WebRools2", "rools http://root.cern.ch/files/pippa.root -l", "WebRools2.ref")
#########################################################################

############################## ROOCP TESTS ##############################
os.system("cp test.root source.root && roocp source.root dest.root")
testCommand("SimpleRoocp", "rools dest.root", "SimpleRools.ref")
testCommand("SimpleRoocp2", "rools dest.root:*", "SimpleRools2.ref")
testCommand("SimpleRoocp3", "rools dest.root:tof", "SimpleRools3.ref")
testCommand("SimpleRoocp4", "rools dest.root:tof/*", "SimpleRools4.ref")
print "Test SimpleRoocp5",
test_nb += 1
if os.path.isfile("source.root") and os.path.isfile("dest.root"):
    print "SUCCESS"
    os.system("rm source.root dest.root")
else:
    print "FAILURE"
    failure_nb += 1
    if os.path.isfile("source.root"):
        os.system("rm source.root")
    if os.path.isfile("dest.root"):
        os.system("rm dest.root")
#########################################################################

############################## ROOMV TESTS ##############################
os.system("cp test.root source.root && roomv source.root dest.root")
testCommand("SimpleRoomv", "rools dest.root", "SimpleRools.ref")
testCommand("SimpleRoomv2", "rools dest.root:*", "SimpleRools2.ref")
testCommand("SimpleRoomv3", "rools dest.root:tof", "SimpleRools3.ref")
testCommand("SimpleRoomv4", "rools dest.root:tof/*", "SimpleRools4.ref")
print "Test SimpleRoomv5",
test_nb += 1
if not os.path.isfile("source.root") and os.path.isfile("dest.root"):
    print "SUCCESS"
    os.system("rm dest.root")
else:
    print "FAILURE"
    failure_nb += 1
    if os.path.isfile("source.root"):
        os.system("rm source.root")
    if os.path.isfile("dest.root"):
        os.system("rm dest.root")
#########################################################################

############################## ROORM TESTS ##############################
os.system("cp test.root victim.root")
testCommand("SimpleRoorm", "roorm -f victim.root:hpx && rools victim.root", "SimpleRoorm.ref")
if os.path.isfile("victim.root"):
    os.system("rm victim.root")
os.system("cp test.root victim.root")
testCommand("SimpleRoorm2", "roorm -f victim.root:tof/plane0 && rools victim.root:tof", "SimpleRoorm2.ref")
if os.path.isfile("victim.root"):
    os.system("rm victim.root")
print "Test SimpleRoorm3",
test_nb += 1
os.system("cp test.root victim.root")
os.system("roorm -f victim.root")
if not os.path.isfile("victim.root"):
    print "SUCCESS"
else:
    print "FAILURE"
    failure_nb += 1
    os.system("rm victim.root")
#########################################################################

############################# ROOMKDIR TESTS ############################
os.system("cp test.root target.root")
testCommand("SimpleRoomkdir", "roomkdir target.root:new_directory && rools target.root", "SimpleRoomkdir.ref")
if os.path.isfile("target.root"):
    os.system("rm target.root")
os.system("cp test.root target.root")
testCommand("SimpleRoomkdir2", "roomkdir target.root:dir/new_directory && rools target.root:dir", "SimpleRoomkdir2.ref")
if os.path.isfile("target.root"):
    os.system("rm target.root")
testCommand("SimpleRoomkdir3", "roomkdir target.root && rools target.root", "SimpleRoomkdir3.ref")
if os.path.isfile("target.root"):
    os.system("rm target.root")
#########################################################################

################################ THE END ################################
print("\nResults :")
print("{0} failure(s) on {1} test(s)".format(failure_nb,test_nb))
#########################################################################
