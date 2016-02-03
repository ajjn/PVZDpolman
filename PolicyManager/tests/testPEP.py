import logging
import logging.config
import os
import re
import shutil
import unittest
import githandler
from invocation import CliPepInvocation
import localconfig
import loggingconfig
import PEP
from samlentitydescriptor import SAMLEntityDescriptor
from userexceptions import InvalidSamlXmlSchemaError

__author__ = 'r2h2'

# Logging setup for unit tests
logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
logging_config = loggingconfig.LoggingConfig(logbasename)
logging.info('DEBUG log: ' + logging_config.LOGFILENAME)

# copy prepared aods from testPMPws
# non-interactive tests run with signxml library + SW-cert; production with MOA + citizen card)
aods_fn_input = 'testdata/PMPws01_aods_%s.xml' % localconfig.AODS_INDICATOR
aods_fn = 'work/PEP03_aods_%s.xml' % localconfig.AODS_INDICATOR
shutil.copyfile(aods_fn_input, aods_fn)


class Test00_cli(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP00: testing CLI interface')
        try:
            cliClient = CliPepInvocation(['-v',
                                          '-x', '-a', 'aods.json',
                                          '--trustedcerts', 'certs.json',
                                          '--pubreq', 'repodir/policydir',
                                          '--list_trustedcerts',
                                          '--loglevel', 'DEBUG', ])
            self.assertEqual(cliClient.args.loglevel, logging.DEBUG)
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')


class Test01_xsdval_valid(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP01: testing schema validation/expecting OK')
        file_handle = open(os.path.abspath('testdata/PAT04_redmineIdentineticsOrg_ed_delete.xml'))
        ed = SAMLEntityDescriptor(file_handle)
        retmsg = ed.validate_xsd()
        file_handle.close()
        self.assertIsNone(retmsg, msg=retmsg)


class Test02_xsdval_invalid(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP02: test calling schema validation/expecting invalid schema(using java SAX parser)')
        with self.assertRaises(InvalidSamlXmlSchemaError) as context:
            with open(os.path.abspath('testdata/PEP02_gondorMagwienGvAt_ed_invalid_xsd.xml')) as f:
                ed = SAMLEntityDescriptor(f)
                retmsg = ed.validate_xsd()


class Test03_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP03: PEP happy cycle')
        repo_dir = 'work/policyDirectory_basic'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath(aods_fn), '-x',
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = githandler.GitHandler(cliClient.args.pubrequ,
                                           init=True,
                                           verbose=cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata(
                'testdata/policyDirectory_basic_%s' % localconfig.AODS_INDICATOR, repo_dir)
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/accepted/PAT02_redmineIdentineticsOrg_ed_req.xml')
        os.path.isfile(requ1_result)
        assert os.path.isfile(os.path.abspath(requ1_result)), 'expected %s in accept directory' % requ1_result


class Test04_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP04: reject a batch of invalid/unauthorized requests')
        repo_dir = 'work/policyDirectory_unauthz_MOA'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath(aods_fn), '-x',
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = githandler.GitHandler(cliClient.args.pubrequ,
                                           init=True,
                                           verbose=cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_unauthz_MOA', repo_dir)
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/rejected/PEP04a_gondorMagwienGvAt_ed_delete.xml')
        os.path.isfile(requ1_result)
        requ2_result = os.path.abspath('work/policyDirectory/rejected/PEP04b_idpExampleCom_req_sig_an.xml')
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ2_result
        requ2_errmsg = 'Signer certificate not found in policy directory'
        with open(requ2_result + '.err') as f:
            assert f.read() == requ2_errmsg, 'expected error log to contain "' + requ2_errmsg + '"'


if __name__ == '__main__':
    unittest.main()
