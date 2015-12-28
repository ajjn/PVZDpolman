import os, sys
import PAtool
import unittest
from invocation import CliPAtoolInvocation
from userExceptions import *

__author__ = 'r2h2'


class Test04_deleteED(unittest.TestCase):
    def runTest(self):
        print('== Test 04: create request to delete EntityDescriptor from metadata')
        entitydescriptor_file = os.path.abspath('testdata/gondorMagwienGvAt_ed_delete.xml')
        md_signingcerts_file = os.path.abspath('testdata/metadatasigningcerts.json')
        cliClient = CliPAtoolInvocation(['-v', '-m', md_signingcerts_file,
                                         'deleteED',
                                         '--entityID', 'https://redmine.identinetics.com',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)


if __name__ == '__main__':
    unittest.main()
