from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CliPmpInvocation
from userExceptions import *
import PMP
__author__ = 'r2h2'
''' all tests not requiring citizen card signature '''

cwd = os.path.dirname(os.path.realpath(__file__))


class Test00_cli(unittest.TestCase):
    def runTest(self):
        print('testing CLI interface for create subcommand .. ', end='')
        try:
            cliClient = CliPmpInvocation(['-v', '-x', '-a', 'aods.json', 'create', ]);
            self.assertEqual(cliClient.args.subcommand, 'create')
            self.assertEqual(cliClient.args.aods, 'aods.json')
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')
        print('OK.')


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        print('== Test 01: happy cycle: create, append, read, verify')
        aodsfile = cwd + '/work/aods_01.json'
        print('removing existing aods file .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'scratch']);
        PMP.run_me(cliClient)
        print('OK.')

        print('creating aods file .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'create']);
        PMP.run_me(cliClient)
        print('OK.')

        inputfile = cwd + '/testdata/a1.json'
        print('appending input file %s .. ' % inputfile, end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile]);
        PMP.run_me(cliClient)
        print('OK.')

        print('reading aods file, writing directory .. ', end='')
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read', \
                                   '--jsondump', cwd + '/work/dir_01.json']);
        PMP.run_me(cliClient)

        print('comparing directory with reference data .. ', end='')
        diff = difflib.ndiff(open(cwd + '/work/dir_01.json').readlines(),
                             open(cwd + '/testdata/dir_01.json').readlines())
        assert sys.stdout.writelines(diff) is None, ' not equal reference data'
        print('OK.')


class Test02_broken_hash_chain(unittest.TestCase):
    def runTest(self):
        print('== Test 02: detect broken hash chain')
        aodsfile = cwd + '/testdata/aods_02.json'
        print('reading aods file with broken hash chain .. ', end='')
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'read']);
        with self.assertRaises(HashChainError) as context:
            PMP.run_me(cliClient)
        print('OK.')


class Test03_broken_input_for_append(unittest.TestCase):
    def runTest(self):
        print('== Test 03: handle broken json input for append')
        aodsfile = cwd + '/work/aods_01.json'
        inputfile = cwd + '/testdata/test03_a1_broken.json'
        print('appending broken input file %s .. ' % inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile]);
        with self.assertRaises(JSONdecodeError) as context:
            PMP.run_me(cliClient)
        print('OK.')


class Test04_broken_input_for_validation(unittest.TestCase):
    def runTest(self):
        print('== Test 04: handle broken input for append/validation')
        aodsfile = cwd + '/work/aods_01.json'
        inputfile = cwd + '/testdata/test04_a01.json'
        print('appending invalid input file ' + inputfile)
        sys.stdout.flush()
        cliClient = CliPmpInvocation(['-v', '-a', aodsfile, 'append', inputfile]);
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
        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig');
        verifier = PvzdVerfiySig(
            "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata/idp5_valid.xml_sig.xml")

        response  = verifier.verify();
        if response.pvzdCode != 'OK': print ('pvzdMessage: ' + response.pvzdMessage)
        self.assertEqual('OK', response.pvzdCode, msg=response.pvzdMessage)

class Test_end(unittest.TestCase):
    def runTest(self):
        print('== Tests completed')
        sys.stdout.flush()


if __name__ == '__main__':
    unittest.main()
