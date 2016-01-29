''' all PMP tests with citizen card signature '''

import difflib, os, sys
#print(os.environ['CLASSPATH'])
import unittest
from assertNoDiff import assertNoDiff
from invocation import CliPmpInvocation
from userexceptions import *
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


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PMPws01: happy cycle: create, append, read, verify (includung xml sig)')
        aodsfile_new = 'work/PMPws01_aods_journal.xml'
        policydir_new = 'work/PMPws01_poldir.json'
        logging.debug('  removing existing aods file %s .. ' % aodsfile_new)
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile_new, '-x', 'scratch'])
        PMP.run_me(cliClient)

        logging.debug('  creating aods file .. ')
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'create']);
        PMP.run_me(cliClient)

        inputfile = os.path.abspath('testdata/PMPns01_pmp_input1.json')
        logging.debug('  appending input file %s .. ' % inputfile)
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'append',
                                      inputfile])
        PMP.run_me(cliClient)

        logging.debug('  reading aods file, writing directory .. ')
        cliClient = CliPmpInvocation(['-v', '-t', 'testdata/trustedcerts.json', '-a', aodsfile_new, '-x', 'read', \
                                   '--poldirjson', policydir_new])
        PMP.run_me(cliClient)
        assertNoDiff('PMPws01_poldir.json')


if __name__ == '__main__':
    unittest.main()
