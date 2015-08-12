from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CLIInvocation
from userExceptions import *
import adminman
__author__ = 'r2h2'
''' all tests that reuqire citizen card signature '''

cwd = os.path.dirname(os.path.realpath(__file__))


class TestS01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        print('== Test S01: happy cycle: create, append, read, verify (incldung xml sig)')
        aodsfile = cwd + '/work/aods_02.xml'
        print('removing existing aods file %s .. ' % aodsfile, end='')
        cliClient = CLIInvocation(['-d', '-a', aodsfile, '-x', 'scratch']);
        adminman.run_me(cliClient)
        print('OK.')

        print('creating aods file .. ', end='')
        cliClient = CLIInvocation(['-d', '-t', '../tests/testdata/trustedcerts.json', '-a', aodsfile, '-x', 'create']);
        adminman.run_me(cliClient)
        print('OK.')

        for i in range(1, 10):
            inputfile = cwd + '/testdata/a%d.json' % i
            print('appending input file %s .. ' % inputfile, end='')
            cliClient = CLIInvocation(['-d', '-a', aodsfile, '-x', 'append', inputfile]);
            adminman.run_me(cliClient)
            print('OK.')

        print('reading aods file, writing directory .. ', end='')
        cliClient = CLIInvocation(['-d', '-t', '../tests/testdata/trustedcerts.json', '-a', aodsfile, 'read', \
                                   '--jsondump', cwd + '/work/dir_01.json']);
        adminman.run_me(cliClient)

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
