from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPmpInvocation
from userExceptions import *
import PMP
__author__ = 'r2h2'
''' all tests that reuqire citizen card signature '''

cwd = os.path.dirname(os.path.realpath(__file__))


class TestS01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        print('== Test S01: happy cycle: create, append, read, verify (incldung xml sig)')
        aodsfile = cwd + '/work/aods_02.xml'
        print('removing existing aods file %s .. ' % aodsfile, end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, '-x', 'scratch']);
        PMP.run_me(cliClient)
        print('OK.')

        print('creating aods file .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-t', '../tests/testdata/trustedcerts.json', '-a', aodsfile, '-x', 'create']);
        PMP.run_me(cliClient)
        print('OK.')

        inputfile = cwd + '/testdata/a1.json'
        print('appending input file %s .. ' % inputfile, end='')
        cliClient = CliPmpInvocation(['-v', '-t', '../tests/testdata/trustedcerts.json',
                                   '-a', aodsfile, '-x', 'append', inputfile]);
        PMP.run_me(cliClient)
        print('OK.')

        print('reading aods file, writing directory .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-t', '../tests/testdata/trustedcerts.json', '-a', aodsfile, '-x', 'read', \
                                   '--jsondump', cwd + '/work/dir_01.json']);
        PMP.run_me(cliClient)

        print('comparing directory with reference data .. ', end='')
        diff = difflib.ndiff(open(cwd + '/work/dir_01.json').readlines(),
                             open(cwd + '/testdata/dir_01.json').readlines())
        assert sys.stdout.writelines(diff) is None, ' not equal reference data'
        print('OK.')


class Test_end(unittest.TestCase):
    def runTest(self):
        print('== Tests completed')
        sys.stdout.flush()


if __name__ == '__main__':
    unittest.main()
