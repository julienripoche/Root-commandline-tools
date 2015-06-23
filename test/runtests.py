#! /usr/bin/env python

import os
import filecmp

def testCommand(testName,command,refFileName):
    ofileName = testName+".out"
    command += " >& %s" %ofileName
    os.system(command)
    print "Test %s" %testName,
    if not filecmp.cmp(ofileName,refFileName):
        print "FAILURE"
    else:
        print "SUCCESS"
    

testCommand("SimpleRools", "rools hsimple.root", "simpleLs.ref")
testCommand("SimpleRools2", "rools hsimple.root:*", "simpleLs2.ref")
