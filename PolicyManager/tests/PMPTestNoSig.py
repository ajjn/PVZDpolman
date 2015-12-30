''' all tests not requiring citizen card signature '''

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

class Test00_cli(unittest.TestCase):
    def runTest(self):
        logging.info('== Test 00: testing CLI interface for create subcommand')
        try:
            cliClient = CliPmpInvocation(['-v', '-x', '-a', 'aods.json', 'create', ])
            self.assertEqual(cliClient.args.subcommand, 'create')
            self.assertEqual(cliClient.args.aods, 'aods.json')
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test 01: happy cycle: create, append, read, verify')
        aodsfile = os.path.abspath('work/aods_01.json')
        logging.debug('=== removing existing aods file .. ')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'scratch'])
        PMP.run_me(cliClient)

        logging.debug('=== creating aods file .. ')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'create'])
        PMP.run_me(cliClient)
        logging.debug('=== create done.')

        inputfile = os.path.abspath('testdata/a1.json')
        logging.debug('=== appending input file %s .. ' % inputfile)
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        PMP.run_me(cliClient)
        logging.debug('=== append done.')

        logging.debug('=== reading aods file, dumping policy directory .. ')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read', '--jsondump', os.path.abspath('work/dir_01.json')])
        PMP.run_me(cliClient)

        logging.debug('comparing directory with reference data .. ')
        diff = difflib.unified_diff(open(os.path.abspath('work/dir_01.json')).readlines(),
                             open(os.path.abspath('testdata/dir_01.json')).readlines())
        assert ''.join(diff) == '', ' result is not equal to reference data'
        logging.debug('=== read/compare done.')


class Test02_broken_hash_chain(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test 02: detect broken hash chain')
        aodsfile = os.path.abspath('testdata/aods_02_broken_hashchain.json')
        logging.debug('reading aods file with broken hash chain .. ')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read'])
        with self.assertRaises(HashChainError) as context:
            PMP.run_me(cliClient)
        logging.debug('OK.')


class Test03_broken_input_for_append(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test 03: handle broken json input for append')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test03_a1_broken.json')
        logging.debug('appending broken input file %s .. ' % inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(JSONdecodeError) as context:
            PMP.run_me(cliClient)
        logging.debug('OK.')


class Test04_broken_input_for_validation(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test 04/1: handle broken input for append/validation: JSON not an array')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a01.json')
        logging.debug('appending invalid input file ' + inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(PMPInputRecNoDict) as context:
            PMP.run_me(cliClient)

        logging.info('  -- Test 04/2: handle broken input for append/validation: missing PK in domain record')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a02.json')
        logging.debug('appending invalid input file ' + inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)

        logging.info('  -- Test 04/3: handle broken input for append/validation: wrong type of PK (bool not String)')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a03.json')
        logging.debug('appending invalid input file ' + inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)

        logging.info('  -- Test 04/4: handle broken input for append/validation: wrong type of PK (int not String)')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a04.json')
        logging.debug('appending invalid input file ' + inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputFormatError) as context:
            PMP.run_me(cliClient)

        logging.info('  -- Test 04/5: handle broken input for append/validation: FK in user privilege references non-existing organization')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a05.json')
        logging.debug('appending invalid input file ' + inputfile)
        logging.info('    expect ERROR message:')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(InputValueError) as context:
            PMP.run_me(cliClient)

class Test05_sigver(unittest.TestCase):
    def runTest(self):
        logging.info('== Test 05: test calling signature verification (java class)')
        # OSX: pyjnius requires dyldlib setting:
        # export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$(/usr/libexec/java_home)/jre/lib/server
        #logging.debug('CLASSPATH=' + os.environ['CLASSPATH'])
        #logging.debug('PYTHONPATH=' + os.environ['PYTHONPATH'])
        #logging.debug('DYLD_LIBRARY_PATH=' + os.environ['DYLD_LIBRARY_PATH'] + '\n')
        from jnius import autoclass

        projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        projdir_abs = os.path.abspath(projdir_rel)

        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
        verifier = PvzdVerfiySig(
            os.path.join(projdir_abs, "conf/moa-spss/MOASPSSConfiguration.xml"),
            os.path.join(projdir_abs, "conf/log4j.properties"),
            os.path.abspath("testdata/idp5_signed_untrusted_signer.xml"))

        response  = verifier.verify()
        if response.pvzdCode != 'OK': print ('pvzdMessage: ' + response.pvzdMessage)
        self.assertEqual('OK', response.pvzdCode, msg=response.pvzdMessage)


if __name__ == '__main__':
    unittest.main()