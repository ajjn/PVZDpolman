import difflib, os, sys
import unittest
from invocation import CliPAtoolInvocation
import PAtool
__author__ = 'r2h2'


class Test01_createED(unittest.TestCase):
    def runTest(self):
        print('== Test 01: create EntitDescriptor from certificate')
        certificate_file = os.path.abspath('testdata/redmineIdentineticsCom-cer.pem')
        entitydescriptor_file = os.path.abspath('work/redmineIdentineticsOrg_ed.xml')
        md_signingcerts_file = os.path.abspath('testdata/metadatasigningcerts.json')
        cliClient = CliPAtoolInvocation(['-v', '-m', md_signingcerts_file,
                                         '-r', 'IDP',
                                         'createED',
                                         certificate_file,
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)


class Test02_signED(unittest.TestCase):
    def runTest(self):
        print('== Test 02: sign EntityDescriptor')
        entitydescriptor_file = os.path.abspath('work/redmineIdentineticsOrg_ed.xml')
        md_signingcerts_file = os.path.abspath('testdata/metadatasigningcerts.json')
        cliClient = CliPAtoolInvocation(['-v', '-m', md_signingcerts_file,
                                         'signED',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)


class Test03_signED_invalidXSD(unittest.TestCase):
    def runTest(self):
        print('== Test 03: sign EntityDescriptor with invlaid SAML schema (OK with xmllint, failing with xerces)')
        entitydescriptor_file = os.path.abspath('testdata/gondorMagwienGvAt_ed_invalid_xsd.xml')
        md_signingcerts_file = os.path.abspath('testdata/metadatasigningcerts.json')
        cliClient = CliPAtoolInvocation(['-v', '-m', md_signingcerts_file,
                                         'signED',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)


if __name__ == '__main__':
    unittest.main()
