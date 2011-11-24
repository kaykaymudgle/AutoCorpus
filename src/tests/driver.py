#!/usr/bin/env python

import sys
from subprocess import check_output
from optparse import OptionParser

def stripLines(text):
    lines = text.split('\n')
    output = ""
    for line in lines:
        output += line.strip() + '\n'
    return output

def performTest(command, expectedOutput):
    print "> " + command
    output = check_output(command, shell=True)
    output = stripLines(output.strip())
    expectedOutput = stripLines(expectedOutput.strip())
    print output + "\n"
    if output != expectedOutput:
        print "ERROR. Expected:"
        print expectedOutput + "\n"
        return False
    else:
        return True

if __name__ == "__main__":    
  parser = OptionParser(usage="%s file" % sys.argv[0])
  (options, args) = parser.parse_args()
  
  if len(args) != 1:
    print "usage: " + parser.usage
    exit(1)

  f = open(args[0], 'r')

  command = None
  expectedOutput = ""
  totalTests = 0
  failedTests = 0
  
  for line in f:
      if line.strip().startswith("#"):
          continue
      elif line.startswith("--"):
          success = performTest(command, expectedOutput)
          totalTests += 1
          failedTests += 0 if success else 1
          command = None
          expectedOutput = ""
      elif command != None:
          expectedOutput += line
      elif len(line.strip()) > 0:
        command = line.strip()

  if command != None:
       success = performTest(command, expectedOutput)
       totalTests += 1
       failedTests += 0 if success else 1      
        
  f.close()
  print "----------------------------"
  print "%-20s %d\n%-20s %d\n%-20s %d" % ("TESTS RUN:", totalTests,
                                 "TESTS PASSED: ", totalTests - failedTests,
                                 "TESTS FAILED:", failedTests)

  exit (0 if failedTests == 0 else 1)