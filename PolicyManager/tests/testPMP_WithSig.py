''' all PMP tests with citizen card signature '''

import difflib
import logging
import logging.config
import os
import re
import sys
import unittest
from assertNoDiff import assertNoDiff
from invocation.clipmp import CliPmp
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
        logging.info('  -- Test PMPws01: happy cycle: create, append, read, verify policy journal sig + struct)')
        pol_journal_fn = 'pol_journal.xml'
        subdir = 'PMP/ws01/'
        pol_journal = os.path.join('work', subdir, pol_journal_fn)
        policyjournal_export = 'work/PMP/ws01/poljournal_export.json'
        policydir_json = 'work/PMP/ws01/poldir.json'
        policydir_html = 'work/PMP/ws01/poldir.html'
        logging.debug('  removing existing aods file %s .. ' % pol_journal)
        cliClient = CliPmp(['-v', '-a', pol_journal, 'scratch'])
        PMP.run_me(cliClient)

        logging.debug('  creating aods file .. ')
        cliClient = CliPmp(['-v', '-t', 'testdata/trustedcerts.json', '-a', pol_journal, 'create']);
        PMP.run_me(cliClient)

        inputfile = os.path.abspath('testdata/PMP/ws01/pmp_initial_policy.json')
        logging.debug('  appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-t', 'testdata/trustedcerts.json', '-a', pol_journal, 'append',
                                      inputfile])
        PMP.run_me(cliClient)

        logging.debug('  reading policy journal, exporting policy journal as json.')
        cliClient = CliPmp(['-v', '-t', 'testdata/trustedcerts.json', '-a', pol_journal, 'read', \
                                   '--journal', policyjournal_export])
        PMP.run_me(cliClient)

        logging.debug('  reading policy journal, exporting policy directory as json.')
        cliClient = CliPmp(['-v', '-t', 'testdata/trustedcerts.json', '-a', pol_journal, 'read', \
                                   '--poldirjson', policydir_json])
        PMP.run_me(cliClient)
        assertNoDiff('poldir.json', subdir=subdir)

        logging.debug('  reading policy journal, exporting policy directory as html.')
        cliClient = CliPmp(['-v', '-t', 'testdata/trustedcerts.json', '-a', pol_journal, 'read', \
                                   '--poldirhtml', policydir_html])
        PMP.run_me(cliClient)


if __name__ == '__main__':
    unittest.main()
