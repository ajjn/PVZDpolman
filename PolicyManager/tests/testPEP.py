import os
import unittest
from githandler import GitHandler
from invocation import CliPepInvocation
import PEP
from samlentitydescriptor import SAMLEntityDescriptor
from userexceptions import InvalidSamlXmlSchemaError

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
                #self.assertIsNotNone(retmsg, msg=retmsg)


class Test03_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP03: PEP happy cycle')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/PMPws01_aods_journal.xml'), '-x',
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_basic', repo_dir)
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)
        requ1_result = os.path.abspath('work/policyDirectory/accepted/PAT02_redmineIdentineticsOrg_ed_req.xml')
        os.path.isfile(requ1_result)
        assert os.path.isfile(os.path.abspath(requ1_result)), 'expected %s in accept directory' % requ1_result


class Test04_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP04: reject a batch of invalid/unauthorized requests')
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/PMPws01_aods_journal.xml'), '-x',
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory_unauthz', repo_dir)
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
