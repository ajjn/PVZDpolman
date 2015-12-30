''' all tests that require citizen card signature '''

from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPmpInvocation
from userExceptions import *
import PMP
__author__ = 'r2h2'

# Logging setup for unit tests
import logging
from logging.config import dictConfig
from settings import *
UT_LOGFILENAME = os.path.abspath(os.path.join('log', __name__ + '.debug'))
UT_LOGGING = LOGGING
UT_LOGGING['handlers']['file']['filename'] = UT_LOGFILENAME
dictConfig(UT_LOGGING)
logging.info('DEBUG log: ' + UT_LOGFILENAME)


class TestS01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('Test S01: happy cycle: create, append, read, verify (includung xml sig)')
        aodsfile_new = 'work/aods_02.xml'
        policydir_new = 'work/dir_02.json'
        logging.debug('removing existing aods file %s .. ' % aodsfile_new)
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile_new, '-x', 'scratch'])
        PMP.run_me(cliClient)
        logging.debug('OK.')

        logging.debug('creating aods file .. ')
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'create']);
        PMP.run_me(cliClient)
        logging.debug('OK.')

        inputfile = os.path.abspath('testdata/a1.json')
        logging.debug('appending input file %s .. ' % inputfile)
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'append',
                                      inputfile])
        PMP.run_me(cliClient)
        logging.debug('OK.')

        logging.debug('reading aods file, writing directory .. ')
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'read', \
                                   '--jsondump', policydir_new])
        PMP.run_me(cliClient)

        logging.debug('comparing directory with reference data .. ')
        aodsfile_refdata = 'testdata/dir_01.json'
        diff = difflib.unified_diff(open(os.path.abspath(policydir_new)).readlines(),
                                    open(os.path.abspath(aodsfile_refdata)).readlines())
        delta = '\n'.join(diff)
        logging.debug(delta)
        assert delta == '', 'resulting policy directory (%s) is not equal to reference data (%s)' % (policydir_new, aodsfile_refdata)
        logging.debug('OK.')


if __name__ == '__main__':
    unittest.main()
