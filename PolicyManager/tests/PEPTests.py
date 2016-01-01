import os
import unittest
from invocation import CliPepInvocation
from SAMLEntityDescriptor import SAMLEntityDescriptor
import PEP
from gitHandler import GitHandler

__author__ = 'r2h2'

projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
projdir_abs = os.path.abspath(projdir_rel)


class Test01_xsdval_valid(unittest.TestCase):
    def runTest(self):
        print('   -- Test PEP01: testing schema validation/expecting OK')
        filename_abs = os.path.abspath('testdata/PEP01_gondorMagwienGvAt_ed_delete.xml')
        ed = SAMLEntityDescriptor(filename_abs, projdir_abs)
        retmsg = ed.validateXSD()
        self.assertIsNone(retmsg, msg=retmsg)


class Test02_xsdval_invalid(unittest.TestCase):
    def runTest(self):
        print('   -- Test PEP02: test calling schema validation/expecting invalid schema(using java SAX parser)')
        filename_abs = os.path.abspath('testdata/PEP02_gondorMagwienGvAt_ed_invalid_xsd.xml')
        ed = SAMLEntityDescriptor(filename_abs, projdir_abs)
        retmsg = ed.validateXSD()
        self.assertIsNotNone(retmsg, msg=retmsg)


class Test04_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        print('  -- Test PEP04: reject a batch of invalid/unauthorized requests')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/aods_peptest.json'),
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        print('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_unauthz', repo_dir)
        print('    - processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/rejected/PEP04a_gondorMagwienGvAt_ed_delete.xml')
        os.path.isfile(requ1_result)
        requ2_result = os.path.abspath('work/policyDirectory/rejected/PEP04b_idp5_valid_sig_untrusted_signer.xml')
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ2_result
        requ2_errmsg = 'Signer certificate not found in policy directory'
        assert open(requ2_result + '.err').read() == requ2_errmsg, 'expected error log to contain "' + requ2_errmsg + '"'


class Test09_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        print('  -- Test PEP09: PEP happy cycle')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/aods_peptest.json'),
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        print('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_basic', repo_dir)
        print('    - processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/accepted/gondorMagwienGvAt_2017_ed_req.xml')
        os.path.isfile(requ1_result)
        assert os.path.isfile(os.path.abspath(requ1_result)), 'expected %s in accept directory' % requ1_result


if __name__ == '__main__':
    unittest.main()
