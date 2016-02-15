import logging
import logging.config
import os
import re
import shutil
import unittest
import constants
import githandler
from invocation.clipep import CliPep
import localconfig
import loggingconfig
import PEP
from samlentitydescriptor import SAMLEntityDescriptor
from userexceptions import *

__author__ = 'r2h2'

# Logging setup for unit tests
logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
logging_config = loggingconfig.LoggingConfig(logbasename)
logging.info('DEBUG log: ' + logging_config.LOGFILENAME)


class Test00_cli(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP00: testing CLI interface')
        try:
            cliClient = CliPep(['-v',
                                '-a', 'aods.json',
                                '--trustedcerts', 'certs.json',
                                '--pepout', 'pepout',
                                '--repodir', 'repodir/policydir',
                                '--list_trustedcerts',
                                '--loglevel', 'DEBUG', ])
            self.assertEqual(cliClient.args.loglevel, logging.DEBUG)
        except SystemExit:
            self.assertTrue(False, meg='System Exit: argparse did not accept parameters (most likely)')


class Test01_xsdval_valid(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP01: testing schema validation/expecting OK')
        file_handle = open(os.path.abspath('testdata/PEP/01/idp5TestExampleOrg_idpXml.xml'))
        ed = SAMLEntityDescriptor(file_handle)
        retmsg = ed.validate_xsd()
        file_handle.close()
        self.assertIsNone(retmsg, msg=retmsg)


class Test02_xsdval_invalid(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP02a: test calling schema validation/expecting invalid root element')
        with self.assertRaises(InputValueError) as context:
            with open(os.path.abspath('testdata/PEP/02/idp6TestExampleOrg_idpXml.xml')) as f:
                ed = SAMLEntityDescriptor(f)
                retmsg = ed.validate_xsd()

        logging.info('  -- Test PEP02b: test calling schema validation/expecting invalid schema')
        with self.assertRaises(InvalidSamlXmlSchemaError) as context:
            with open(os.path.abspath('testdata/PEP/02/idp7TestExampleOrg_idpXml.xml')) as f:
                ed = SAMLEntityDescriptor(f)
                retmsg = ed.validate_xsd()


class Test03_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP03: PEP happy cycle')
        repo_dir = 'work/PEP/03/policyDirectory_basic_' + localconfig.AODS_INDICATOR
        pepoutdir = 'work/PEP/03/pepout/'
        request_queue = os.path.join(repo_dir, constants.GIT_REQUESTQUEUE)
        cliClient = CliPep(['--verbose',
                            '--aods', os.path.join(repo_dir, constants.GIT_POLICYDIR, 'pol_journal.xml'), 
                            '--pepoutdir', pepoutdir,
                            '--repodir', os.path.abspath(repo_dir),
                            '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = githandler.GitHandler(cliClient.args.repodir,
                                           pepoutdir,
                                           init=True,
                                           verbose=cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata(
                'testdata/PEP/03/policyDirectory_basic_%s' % localconfig.AODS_INDICATOR, repo_dir)
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)

        for fn in ('gondorWienGvAt_idp.xml',
                   'redmineIdentineticsCom_idp.xml',
                   'wwwTestPortalverbundGvAt.xml'):
            requ1_source = os.path.join(request_queue, fn)
            requ1_result = os.path.join(pepoutdir, fn)
            assert os.path.isfile(requ1_result), 'expected %s in pepoutdir directory: ' % requ1_result
            assert not os.path.isfile(requ1_source), 'expected %s not to be in request_queue: ' % requ1_result

        for fn in ('redmineIdentineticsOrg_req.xml', ):
            requ1_source = os.path.join(request_queue, fn)
            requ1_result = os.path.join(repo_dir, constants.GIT_REJECTED, fn)
            assert os.path.isfile(requ1_result), 'expected %s in rejected directory: ' % requ1_result
            assert not os.path.isfile(requ1_source), 'expected %s not to be in request_queue: ' % requ1_result



class Test04_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP04: reject a batch of invalid/unauthorized requests')
        repo_dir = 'work/PEP/04/policyDirectory_unauth_' + localconfig.AODS_INDICATOR
        pepoutdir = 'work/PEP/04/pepout/'
        cliClient = CliPep(['--verbose',
                            '--aods', os.path.join(repo_dir, constants.GIT_POLICYDIR, 'pol_journal.xml'), 
                            '--pepoutdir', pepoutdir,
                            '--repodir', os.path.abspath(repo_dir),
                            '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - creating fresh git repo in ' + repo_dir + ', adding test data')
        gitHandler = githandler.GitHandler(cliClient.args.repodir,
                                           pepoutdir,
                                           init=True,
                                           verbose=cliClient.args.verbose)
        gitHandler.reset_repo_with_defined_testdata(
                'testdata/PEP/04/policyDirectory_unauthz_%s' % localconfig.AODS_INDICATOR, repo_dir)
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)

        requ1_result = os.path.abspath('%s/rejected/gondorWienGvAt_delete.xml' % repo_dir)
        os.path.isfile(requ1_result)

        requ2_result = os.path.abspath('%s/rejected/idpExampleCom_idpXml.xml' % repo_dir)
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ2_result
        requ2_errmsg = 'Signer certificate not found in policy directory'
        with open(requ2_result + '.err') as f:
            assert f.read() == requ2_errmsg, 'expected error log to contain "' + requ2_errmsg + '"'

        requ3_result = os.path.abspath('%s/rejected/idpExampleCom_idpXmlUnsigned.xml' % repo_dir)
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ3_result
        requ3_errmsg = 'Signature verification failed'
        with open(requ3_result + '.err') as f:
            assert f.read().startswith(requ3_errmsg), 'expected error log to contain "' + requ3_errmsg + '"'

        requ4_result = os.path.abspath('%s/rejected/fatamorganaIdentineticsCom.xml' % repo_dir)
        assert os.path.isfile(os.path.abspath(requ2_result)), 'expected %s in reject directory' % requ3_result
        requ4_errmsg = 'rejected deletion request for non existing EntityDescriptor'
        with open(requ4_result + '.err') as f:
            assert f.read().startswith(requ4_errmsg), 'expected error log to contain "' + requ3_errmsg + '"'


class Test05_delete_ok_cycle(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP05: PEP delete ok cycle')
        repo_dir = 'work/PEP/03/policyDirectory_basic_' + localconfig.AODS_INDICATOR
        pepoutdir = 'work/PEP/03/pepout/'
        cliClient = CliPep(['--verbose',
                            '--aods', os.path.join(repo_dir, constants.GIT_POLICYDIR, 'pol_journal.xml'),
                            '--pepoutdir', pepoutdir,
                            '--repodir', os.path.abspath(repo_dir),
                            '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        logging.debug('    - adding to test 03 git repo in ' + repo_dir)
        gitHandler = githandler.GitHandler(cliClient.args.repodir,
                                           pepoutdir,
                                           init=False,
                                           verbose=cliClient.args.verbose)
        gitHandler.add_request_message('testdata/PEP/05/wwwTestPortalverbundGvAt.xml')
        logging.debug('    - processing request queue')
        PEP.run_me(cliClient)

        for fn in ('wwwTestPortalverbundGvAt.xml', ):
            requ1_result = os.path.join(pepoutdir, fn)
            assert not os.path.isfile(requ1_result), 'expected %s not to be in pepoutdir directory: ' % requ1_result
            requ2_result = os.path.join(repo_dir, constants.GIT_DELETED, fn)
            assert os.path.isfile(requ2_result), 'expected %s in "deleted" repo sub-directory: ' % requ2_result


if __name__ == '__main__':
    unittest.main()
