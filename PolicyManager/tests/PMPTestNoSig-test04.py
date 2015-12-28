from __future__ import print_function
import difflib, os, sys
import unittest
#for e in os.environ:
#    print(e + '=' + os.environ[e])
#print('CLASSPATH=' + os.environ['CLASSPATH'])
#print('PYTHONPATH=' + os.environ['PYTHONPATH'])
#print('JAVA_HOME=' + os.environ['JAVA_HOME'])
print('---')
from invocation import CliPmpInvocation
from userExceptions import *
import PMP
__author__ = 'r2h2'
''' all tests not requiring citizen card signature '''


class Test04_broken_input_for_validation(unittest.TestCase):
    def runTest(self):
        print('== Test 04/1: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a01.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(PMPInputRecNoDict) as context:
            PMP.run_me(cliClient)

        print('== Test 04/2: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a02.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)

        print('== Test 04/3: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a03.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)

        print('== Test 04/4: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a04.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)

        print('== Test 04/5: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a05.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)



if __name__ == '__main__':
    unittest.main()
