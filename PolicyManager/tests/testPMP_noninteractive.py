''' all tests not requiring citizen card signature '''
import difflib
import logging
import logging.config
import os
import re
import sys
import unittest
import warnings
from assertNoDiff import assertNoDiff
from invocation.clipmp import CliPmp
import loggingconfig
from userexceptions import *
import PMP
__author__ = 'r2h2'

# Logging setup for unit tests
logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
logging_config = loggingconfig.LoggingConfig(logbasename, mode='w')
logging.info('DEBUG log: ' + logging_config.LOGFILENAME)

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            test_func(self, *args, **kwargs)
    return do_test

class Test00_cli(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PMPns00: testing CLI interface for create subcommand')
        try:
            cliClient = CliPmp(['-v', '-n', '-n', '-a', 'aods.json', 'create', ])
            self.assertEqual(cliClient.args.subcommand, 'create')
            self.assertEqual(cliClient.args.aods, 'aods.json')
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')


class Test01_basic_happy_cycle(unittest.TestCase):
    @ignore_warnings
    def runTest(self):
        logging.info('  -- Test PMPns01: happy cycle: create, append, read, verify')
        policy_journal = os.path.abspath('work/PMP/ns01/aods.json')
        logging.debug('=== removing existing aods file .. ')
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'scratch'])
        PMP.run_me(cliClient)

        logging.debug('=== creating aods file .. ')
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'create'])
        PMP.run_me(cliClient)
        logging.debug('=== create done.')

        inputfile = os.path.abspath('testdata/PMP/ns01/append01_OK.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'append', inputfile])
        PMP.run_me(cliClient)
        logging.debug('=== append done.')

        inputfile = os.path.abspath('testdata/PMP/ns01/append02_delete_non_exist_rec.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)
        logging.debug('=== append done.')

        inputfile = os.path.abspath('testdata/PMP/ns01/append03_delete_non_exist_orgid.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)
        logging.debug('=== append done.')

        inputfile = os.path.abspath('testdata/PMP/ns01/append04_OK.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'append', inputfile])
        PMP.run_me(cliClient)
        logging.debug('=== append done.')

        logging.debug('=== reading & dumping policy journal as json, directory as json & html .. ')
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'read',
                            '--poldirjson', os.path.abspath('work/PMP/ns01/poldir1.json'),
                            '--poldirhtml', os.path.abspath('work/PMP/ns01/poldir1.html'),
                            '--journal', os.path.abspath('work/PMP/ns01/pol_journal1.json')])
        PMP.run_me(cliClient)
        assertNoDiff('poldir1.json', subdir='PMP/ns01')

        inputfile = os.path.abspath('testdata/PMP/ns01/append05_OK.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'append', inputfile])
        PMP.run_me(cliClient)
        logging.debug('=== append done.')

        logging.debug('=== reading & dumping policy journal as json, directory as json & html .. ')
        cliClient = CliPmp(['-v', '-n', '-a', policy_journal, 'read',
                            '--poldirjson', os.path.abspath('work/PMP/ns01/poldir2.json'),
                            '--poldirhtml', os.path.abspath('work/PMP/ns01/poldir2.html'),
                            '--journal', os.path.abspath('work/PMP/ns01/pol_journal2.json')])
        PMP.run_me(cliClient)
        assertNoDiff('poldir2.json', subdir='PMP/ns01')


class Test02_broken_hash_chain(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PMPns02: detect broken hash chain')
        aodsfile = os.path.abspath('testdata/PMP/ns02/aods_broken_hashchain.json')
        logging.debug('reading aods file with broken hash chain .. ')
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'read'])
        with self.assertRaises(HashChainError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])


class Test03_broken_input_for_append(unittest.TestCase):
    @ignore_warnings
    def runTest(self):
        logging.info('  -- Test PMPns03: handle broken json input for append')
        aodsfile = os.path.abspath('work/PMP/ns01/aods.json')
        inputfile = os.path.abspath('testdata/PMP/ns03/pmpinput_brokenjson.json')
        logging.debug('appending broken input file %s .. ' % inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(JSONdecodeError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + ''.join(context.exception.args))


class Test04_broken_input_for_validation(unittest.TestCase):
    @ignore_warnings
    def runTest(self):
        logging.info('  -- Test PMPns04/1: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/PMP/ns01/aods.json')
        inputfile = os.path.abspath('testdata/PMP/ns04/pmpinput_noarray.json')
        logging.debug('appending invalid input file ' + inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(PMPInputRecNoDictError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])

        logging.info('  -- Test PMPns04/2: handle broken input for append/validation: FK references non-existing domain')
        inputfile = os.path.abspath('testdata/PMP/ns04/pmpinput_fk_invalid_domain.json')
        logging.debug('appending invalid input file ' + inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])

        logging.info('  -- Test PMPns04/3: handle broken input for append/validation: wrong type of PK (bool not String)')
        inputfile = os.path.abspath('testdata/PMP/ns04/pmpinput_pk_no_str.json')
        logging.debug('appending invalid input file ' + inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])

        logging.info('  -- Test PMPns04/4: handle broken input for append/validation: wrong type of PK (int not String)')
        inputfile = os.path.abspath('testdata/PMP/ns04/pmpinput_pk_no_str.json.json')
        logging.debug('appending invalid input file ' + inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])

        logging.info('  -- Test PMPns04/5: handle broken input for append/validation: FK in user privilege references non-existing organization')
        inputfile = os.path.abspath('testdata/PMP/ns04/pmpinput_fk_invalid_org.json.json')
        logging.debug('appending invalid input file ' + inputfile)
        cliClient = CliPmp(['-v', '-n', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)
        logging.debug('Expected exception caught: ' + str(context.expected) + ': ' + context.exception.args[0])

# removed - covered py PMPws01
# class Test05_sigver(unittest.TestCase):
#     def runTest(self):
#         logging.info('  -- Test PMPns05: test calling signature verification (java class)')
#         # OSX: pyjnius requires dyldlib setting:
#         # export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$(/usr/libexec/java_home)/jre/lib/server
#         #logging.debug('CLASSPATH=' + os.environ['CLASSPATH'])
#         #logging.debug('PYTHONPATH=' + os.environ['PYTHONPATH'])
#         #logging.debug('DYLD_LIBRARY_PATH=' + os.environ['DYLD_LIBRARY_PATH'] + '\n')
#         from jnius import autoclass
#
#         projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#         projdir_abs = os.path.abspath(projdir_rel)
#
#         PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
#         verifier = PvzdVerfiySig(
#             os.path.join(projdir_abs, "conf/moa-spss/MOASPSSConfiguration.xml"),
#             os.path.join(projdir_abs, "conf/log4j.properties"),
#             os.path.abspath("testdata/PMPns05_idp5_signed_untrusted_signer.xml"))
#
#         response  = verifier.verify()
#         if response.pvzdCode != 'OK': print ('pvzdMessage: ' + response.pvzdMessage)
#         self.assertEqual('OK', response.pvzdCode, msg=response.pvzdMessage)


if __name__ == '__main__':
    unittest.main()
