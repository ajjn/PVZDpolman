import difflib, os, sys
import unittest
from invocation import CliPAtoolInvocation
import PAtool
__author__ = 'r2h2'


class Test01_createED(unittest.TestCase):
    def runTest(self):
        print('== Test 01: not implemented yet')


class Test02_signED(unittest.TestCase):
    def runTest(self):
        print('== Test 02: sign EntityDescriptor')
        entitydescriptor_file = os.path.abspath('testdata/idpExampleOrg_unsigned.xml')
        md_signingcerts_file = os.path.abspath('testdata/metadatasigningcerts.json')
        cliClient = CliPAtoolInvocation(['-v', '-m', md_signingcerts_file, 'signED', entitydescriptor_file])
        PAtool.run_me(cliClient)


if __name__ == '__main__':
    unittest.main()
