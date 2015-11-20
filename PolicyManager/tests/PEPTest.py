import os
import unittest
from invocation import CliPepInvocation
import PEP
from gitHandler import GitHandler
__author__ = 'r2h2'

projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
projdir_abs = os.path.abspath(projdir_rel)


class Test01_valxsd(unittest.TestCase):
    def runTest(self):
        print('== Test 01: testing xsd validator (java class)')
        from jnius import autoclass
        XmlValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XmlValidator')
        validator = XmlValidator(os.path.join(projdir_abs, 'ValidateXSD/SAML_MD_Schema'), True)
        print('=== testing with valid file')
        m = validator.validateSchema(os.path.abspath('testdata/idp5_valid_xml_unsigned.xml'))
        self.assertIsNone(m, 'expected empty message, but received: ' + str(m))
        print('=== testing with invalid file')
        m = validator.validateSchema(os.path.abspath('testdata/idp5_invalid_xml.xml'))
        self.assertIsNotNone(m, 'expected empty message, but received: ' + str(m))


class Test02_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        import PEP
        from gitHandler import GitHandler
        print('\n== Test02: PEP happy cycle')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/aods_peptest.json'),
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        print('=== creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_basic', repo_dir)
        print('=== processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/accepted/gondorMagwienGvAt_2017_ed_req.xml')
        os.path.isfile(requ1_result)
        assert os.path.isfile(os.path.abspath(requ1_result)), 'expected %s in accept directory' % requ1_result

class Test03_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        import PEP
        from gitHandler import GitHandler
        print('\n== Test02: PEP happy cycle')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/aods_peptest.json'),
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        print('=== creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_unauthz', repo_dir)
        print('=== processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/rejected/01_idp5_valid_nosig.xml')
        os.path.isfile(requ1_result)
        requ2_result = os.path.abspath('work/policyDirectory/rejected/02_idp5_valid_sig_untrusted_signer.xml')
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ2_result
        requ2_errmsg = 'Signer certificate not found in policy directory'
        assert open(requ2_result + '.err').read() == requ2_errmsg, 'expected error log to contain "' + requ2_errmsg + '"'

if __name__ == '__main__':
    unittest.main()
