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

def setUpModule():
    try:
        os.environ['PYJNIUS_ACTIVATE']
    except KeyError:
        import javabridge
        try:
            # include user added classpath
            classpath = os.environ['CLASSPATH']
            classpath = classpath.split(os.pathsep)
            javabridge.JARS.extend(classpath)
        except KeyError:
            None

        javabridge.start_vm()
        javabridge.attach()


def tearDownModule():
    try:
        os.environ['PYJNIUS_ACTIVATE']
    except KeyError:
        import javabridge
        javabridge.detach()
        javabridge.kill_vm()

# Logging setup for unit tests
logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
logging_config = loggingconfig.LoggingConfig(logbasename)
logging.info('DEBUG log: ' + logging_config.LOGFILENAME)
here = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
version = open(os.path.join(here, 'VERSION')).read()
projname = open(os.path.join(here, 'PROJNAME')).read()
logging.info(projname + ' V' + version)


def make_dirs(path, dir=False) -> str:
    """ create directories in the path that do not exist (if path is directory, it must have a trailing / """
    if dir:
        os.makedirs(path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


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
        pepoutdir = make_dirs('work/PEP/03/pepout/', dir=True)
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



class Test04_unauthorized_requests(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PEP04: reject a batch of invalid/unauthorized requests')
        repo_dir = 'work/PEP/04/policyDirectory_unauth_' + localconfig.AODS_INDICATOR
        request_queue = os.path.join(repo_dir, constants.GIT_REQUESTQUEUE)
        pepoutdir = make_dirs('work/PEP/04/pepout/', dir=True)
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

        # ttab is a list of 2-tuples containing file expected in the reject dir, and
        # the start of the accompaning error message
        ttab = (('fatamorganaIdentineticsCom.xml','rejected deletion request for non existing EntityDescriptor'),
                ('gondorWienGvAt_delete.xml','Invalid format for EntitiyDescriptor filename'),
                ('idpExampleCom_idpXmlUnsigned.xml','Signature verification failed'),
                ('idpExampleCom_idpXml.xml','Signer certificate not found in policy directory'),
                ('redmineIdentineticsOrg_req.xml', 'Invalid format for EntitiyDescriptor filename'),
                )

        for (fn, requ_errmsg) in ttab:
            requ_srcpath = os.path.join(request_queue, fn)
            requ_destpath = os.path.join(repo_dir, constants.GIT_REJECTED, fn)
            assert os.path.isfile(requ_destpath), 'expected %s in rejected directory: ' % requ_destpath
            assert not os.path.isfile(requ_srcpath), '%s should not be left in request_queue: ' % requ_destpath
            with open(requ_destpath + '.err') as f:
                assert f.read().startswith(requ_errmsg), 'expected error log to contain "' + \
                                                         requ_errmsg + '" for file ' + fn


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
    unittest.main(warnings='ignore')
