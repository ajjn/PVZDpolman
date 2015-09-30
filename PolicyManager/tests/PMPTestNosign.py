from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPmpInvocation
from userExceptions import *
import PMP
__author__ = 'r2h2'
''' all tests not requiring citizen card signature '''

#cwd = os.path.dirname(os.path.realpath(__file__))


class Test00_cli(unittest.TestCase):
    def runTest(self):
        print('== Test 00: testing CLI interface for create subcommand .. ', end='')
        try:
            cliClient = CliPmpInvocation(['-v', '-x', '-a', 'aods.json', 'create', ])
            self.assertEqual(cliClient.args.subcommand, 'create')
            self.assertEqual(cliClient.args.aods, 'aods.json')
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')
        print('OK.')


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        print('== Test 01: happy cycle: create, append, read, verify')
        aodsfile = os.path.abspath('work/aods_01.json')
        print('=== removing existing aods file .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'scratch'])
        PMP.run_me(cliClient)
        print('=== done.')

        print('=== creating aods file .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'create'])
        PMP.run_me(cliClient)
        print('=== create done.')

        inputfile = os.path.abspath('testdata/a1.json')
        print('=== appending input file %s .. ' % inputfile, end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        PMP.run_me(cliClient)
        print('=== append done.')

        print('=== reading aods file, dumping policy directory .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read', '--jsondump', os.path.abspath('work/dir_01.json')])
        PMP.run_me(cliClient)

        print('comparing directory with reference data .. ', end='')
        diff = difflib.unified_diff(open(os.path.abspath('work/dir_01.json')).readlines(),
                             open(os.path.abspath('testdata/dir_01.json')).readlines())
        assert ''.join(diff) == '', ' result is not equal to reference data'
        print('=== read/compare done.')


class Test02_broken_hash_chain(unittest.TestCase):
    def runTest(self):
        print('== Test 02: detect broken hash chain')
        aodsfile = os.path.abspath('testdata/aods_02_broken_hashchain.json')
        print('reading aods file with broken hash chain .. ', end='')
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read'])
        with self.assertRaises(HashChainError) as context:
            PMP.run_me(cliClient)
        print('OK.')


class Test03_broken_input_for_append(unittest.TestCase):
    def runTest(self):
        print('== Test 03: handle broken json input for append')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test03_a1_broken.json')
        print('appending broken input file %s .. ' % inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(JSONdecodeError) as context:
            PMP.run_me(cliClient)
        print('OK.')


class Test04_broken_input_for_validation(unittest.TestCase):
    def runTest(self):
        print('== Test 04: handle broken input for append/validation')
        aodsfile = os.path.abspath('work/aods_01.json')
        inputfile = os.path.abspath('testdata/test04_a01.json')
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile])
        with self.assertRaises(AssertionError) as context:
            PMP.run_me(cliClient)


class Test05_sigver(unittest.TestCase):
    def runTest(self):
        print('== Test 05: test calling signature verification (java class)')
        # OSX: pyjnius requires dyblib setting, e.g.:
        # export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$(/usr/libexec/java_home)/jre/lib/server
        #print('CLASSPATH=' + os.environ['CLASSPATH'])
        #print('PYTHONPATH=' + os.environ['PYTHONPATH'])
        #print('DYLD_LIBRARY_PATH=' + os.environ['DYLD_LIBRARY_PATH'] + '\n')
        from jnius import autoclass

        # set classpath to include MOA-SS
        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
        verifier = PvzdVerfiySig(
            "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata/idp5_signed_untrusted_signer.xml")

        response  = verifier.verify()
        if response.pvzdCode != 'OK': print ('pvzdMessage: ' + response.pvzdMessage)
        self.assertEqual('OK', response.pvzdCode, msg=response.pvzdMessage)


if __name__ == '__main__':
    unittest.main()
