#! /usr/bin/env python

import os
import filecmp

def testCommand(testName,command,refFileName):
    ofileName = testName+".out"
    command += " >& %s" %ofileName
    os.system(command)
    print "Test %s" %testName,
    if filecmp.cmp(ofileName,refFileName):
        print "SUCCESS"
    else:
        print "FAILURE"

testCommand("SimpleRools", "rools test.root", "SimpleRools.ref")
testCommand("SimpleRools2", "rools test.root:*", "SimpleRools2.ref")
testCommand("SimpleRools3", "rools test.root:tof", "SimpleRools3.ref")
testCommand("SimpleRools4", "rools test.root:tof/*", "SimpleRools4.ref")

testCommand("LongRools", "rools -l test.root", "LongRools.ref")
testCommand("LongRools2", "rools -l test.root:*", "LongRools2.ref")
testCommand("LongRools3", "rools -l test.root:tof", "LongRools3.ref")
testCommand("LongRools4", "rools -l test.root:tof/*", "LongRools4.ref")
