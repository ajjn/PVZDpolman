from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPepInvocation
import PEP
__author__ = 'r2h2'

cwd = os.path.dirname(os.path.realpath(__file__))


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):

        print('reading aods file, writing directory .. ', end='')
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', cwd + '/testdata/aods_peptest.json',
                                      '--pubreq', cwd + '/testdata/pub_requests', \
                                      '--trustedcerts', cwd + '/testdata/trustedcerts.json']);
        PEP.run_me(cliClient)

        print('comparing directory with reference data .. ', end='')
        diff = difflib.ndiff(open(cwd + '/work/dir_01.json').readlines(),
                             open(cwd + '/testdata/dir_01.json').readlines())
        assert sys.stdout.writelines(diff) is None, ' not equal reference data'
        print('OK.')


if __name__ == '__main__':
    unittest.main()
