from __future__ import print_function
import difflib, os, sys
import unittest
from invocation import CLIInvocation
from userExceptions import *
import adminman
__author__ = 'r2h2'
''' all tests not requiring citizen card signature '''

cwd = os.path.dirname(os.path.realpath(__file__))


class Test00_cli(unittest.TestCase):
    def runTest(self):
        print('testing CLI interface for create subcommand .. ', end='')
        try:
            cliClient = CLIInvocation(['-d', '-x', '-a', 'aods.json', 'create', ]);
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
        cliClient = CLIInvocation(['-d', '-a', aodsfile, 'scratch']);
        adminman.run_me(cliClient)
        print('OK.')

        print('creating aods file .. ', end='')
        cliClient = CLIInvocation(['-d', '-a', aodsfile, 'create']);
        adminman.run_me(cliClient)
        print('OK.')

        for i in range(1, 10):
            inputfile = cwd + '/testdata/a%d.json' % i
            print('appending input file %s .. ' % inputfile, end='')
            cliClient = CLIInvocation(['-d', '-a', aodsfile, 'append', inputfile]);
            adminman.run_me(cliClient)
            print('OK.')

        print('reading aods file, writing directory .. ', end='')
        cliClient = CLIInvocation(['-d', '-a', aodsfile, 'read', \
                                   '--jsondump', cwd + '/work/dir_01.json']);
        adminman.run_me(cliClient)

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
        cliClient = CLIInvocation(['-d', '-a', aodsfile, 'read']);
        with self.assertRaises(HashChainError) as context:
            adminman.run_me(cliClient)
        print('OK.')


class Test03_broken_input_for_append(unittest.TestCase):
    def runTest(self):
        print('== Test 03: handle broken input for append')
        aodsfile = cwd + '/work/aods_01.json'
        inputfile = cwd + '/testdata/test03_a1_broken.json'
        print('appending broken input file %s .. ' % inputfile, end='')
        sys.stdout.flush()
        cliClient = CLIInvocation(['-d', '-a', aodsfile, 'append', inputfile]);
        with self.assertRaises(JSONdecodeError) as context:
            adminman.run_me(cliClient)
        print('OK.')


class Test04_broken_input_for_validation(unittest.TestCase):
    def runTest(self):
        print('== Test 04: handle broken input for append/validation')
        aodsfile = cwd + '/work/aods_01.json'
        for i in range(1, 6):
            inputfile = cwd + '/testdata/test04_a0%s.json' % i
            print('appending invalid input file ' + inputfile)
            sys.stdout.flush()
            cliClient = CLIInvocation(['-d', '-a', aodsfile, 'append', inputfile]);
            with self.assertRaises(InputFormatOrValueError) as context:
                adminman.run_me(cliClient)


class Test05_sigver(unittest.TestCase):
    def runTest(self):
        print('== Test 05: test calling signature verification (java class)')
        # OSX: pyjnius requires dyblib setting, e.g.:
        # export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$(/usr/libexec/java_home)/jre/lib/server
        from jnius import autoclass

        # set classpath to include MOA-SS
        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.PvzdVerfiySig');
        verifier = PvzdVerfiySig(
            "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties",
            "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata/idp5_valid.xml_sig.xml")

        response  = verifier.verify();
        self.assertEqual('OK', response.pvzdCode)


class Test_end(unittest.TestCase):
    def runTest(self):
        print('== Tests completed')
        sys.stdout.flush()


if __name__ == '__main__':
    unittest.main()
