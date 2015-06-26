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

testCommand("SimpleRools", "rools test.root", "SimpleRools.ref")
testCommand("SimpleRools2", "rools test.root:*", "SimpleRools2.ref")
testCommand("SimpleRools3", "rools test.root:tof", "SimpleRools3.ref")
testCommand("SimpleRools4", "rools test.root:tof/*", "SimpleRools4.ref")

testCommand("LongRools", "rools -l test.root", "LongRools.ref")
testCommand("LongRools2", "rools -l test.root:*", "LongRools2.ref")
testCommand("LongRools3", "rools -l test.root:tof", "LongRools3.ref")
testCommand("LongRools4", "rools -l test.root:tof/*", "LongRools4.ref")

print("{0} failure(s) on {1} test(s)".format(failure_nb,test_nb))
