''' all PMP tests with citizen card signature '''

import difflib
import logging
import logging.config
import os
import re
import sys
import unittest
from assertNoDiff import assertNoDiff
from invocation import CliPmpInvocation
import localconfig
import loggingconfig
from userexceptions import *
import PMP
__author__ = 'r2h2'

# Logging setup for unit tests
logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
logging_config = loggingconfig.LoggingConfig(logbasename)
logging.info('DEBUG log: ' + logging_config.LOGFILENAME)


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PMPws01: happy cycle: create, append, read, verify (including xml sig)')
        aodsfile_new = 'work/policyDirectory/policydir/PMPws01_aods_%s.xml' % localconfig.AODS_INDICATOR
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
