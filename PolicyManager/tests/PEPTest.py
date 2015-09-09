from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPepInvocation
import PEP
__author__ = 'r2h2'

cwd = os.path.dirname(os.path.realpath(__file__))


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):

        print('processing request queue .. ', end='')
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', cwd + '/testdata/aods_peptest.json',
                                      '--pubreq', cwd + '/testdata/policyDirectory',
                                      '--trustedcerts', cwd + '/testdata/trustedcerts.json'])
        PEP.run_me(cliClient)



if __name__ == '__main__':
    unittest.main()
