import difflib
import logging
import logging.config
import lxml.etree
import os
import re
import sys
import unittest
from assertNoDiff import assertNoDiff
from invocation.clipatool import CliPatool
import loggingconfig
import PAtool
from userexceptions import *

__author__ = 'r2h2'

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

class Test01_createED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT01: create EntitDescriptor from certificate (pvzd:pvptype="R-Profile")')
        certificate_file = os.path.abspath('testdata/PAT/01/redmineIdentineticsCom-cer.pem')
        entitydescriptor_file = 'redmineIdentineticsCom_idpXml.unsigned.xml'
        output_dir = make_dirs(os.path.abspath('work/PAT/01/'), dir=True)
        cliClient = CliPatool(['-v', 'createED',
                            '-e', 'https://redmine.identinetics.com/idp.xml',
                            '-r', 'IDP',
                            '-o', output_dir,
                            certificate_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(entitydescriptor_file), subdir='PAT/01')


class Test02_signED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT02a: sign EntityDescriptor w/o xml header to default output')
        entitydescriptor_file = os.path.abspath('testdata/PAT/02/redmineIdentineticsOrg_ed.xml')
        output_dir = make_dirs(os.path.abspath('work/PAT/02/'), dir=True)
        cliClient = CliPatool(['-v', 'signED', '-o', output_dir, entitydescriptor_file])
        PAtool.run_me(cliClient)

        logging.info('  -- Test PAT02b: sign EntityDescriptor with xml header to specified output')
        entitydescriptor_file = os.path.abspath('testdata/PAT/02/idpExampleCom_unsigned.xml')
        entitydescriptor_sig_file = os.path.abspath('work/PAT/02/idpExampleCom.xml')
        cliClient = CliPatool(['-v', 'signED', '-o', output_dir, entitydescriptor_file])
        PAtool.run_me(cliClient)
        # skipping comparison with ref data: signatures are time-stamped, would need xpath filter ..

class Test03_signED_invalidXSD(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT03a: sign EntityDescriptor with invalid SAML schema (OK with xmllint, failing with xerces)')
        entitydescriptor_file = os.path.abspath('testdata/PAT/03/gondorWienGvAt_invalidXsd.xml')
        output_dir = make_dirs(os.path.abspath('work/PAT/03/'), dir=True)
        cliClient = CliPatool(['-v', 'signED', '-o', output_dir, entitydescriptor_file])
        with self.assertRaises(InvalidSamlXmlSchemaError) as context:
            PAtool.run_me(cliClient)

        logging.info('  -- Test PAT03b: root is not md:EntityDescriptor')
        entitydescriptor_file = os.path.abspath('testdata/PAT/03/gondorMagwienGvAt_enveloping_sig.xml')
        cliClient = CliPatool(['-v', 'signED', '-o', output_dir, entitydescriptor_file])
        with self.assertRaises(InputValueError) as context:
            PAtool.run_me(cliClient)

        logging.info('  -- Test PAT03c: EntityDescriptor not root (enveloping signature)')
        entitydescriptor_file = os.path.abspath('testdata/PAT/03/gondorWienGvAt_invalidXml.xml')
        cliClient = CliPatool(['-v', 'signED', '-o', output_dir, entitydescriptor_file])
        with self.assertRaises(lxml.etree.XMLSyntaxError) as context:
            PAtool.run_me(cliClient)
        sys.tracebacklimit = 1000


class Test04_deleteED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT04: create request to delete EntityDescriptor from metadata')
        entitydescriptor_file = os.path.abspath('work/PAT/04/redmineIdentineticsOrg_IdpXml.xml')
        output_dir = make_dirs(os.path.abspath('work/PAT/04/'), dir=True)
        cliClient = CliPatool(['-v', 'deleteED',
                               '--entityid', 'https://redmine.identinetics.com/idp.xml',
                               '--outputdir', output_dir])
        PAtool.run_me(cliClient)
        os.path.exists(entitydescriptor_file)


class Test05_revokeCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT05: create PMP import file to revoke a certificate')
        certificate_file = os.path.abspath('testdata/PAT/05/gondorMagwienGvAt_2011-cer.pem')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/05/gondorMagwienGvAt_2011-cer_revoke.json'))  # output
        cliClient = CliPatool(['-v', 'revokeCert',
                               '--certfile', certificate_file,
                               '--reason', 'testing revocation',
                               pmpinput_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(pmpinput_file), subdir='PAT/05')


class Test06_caCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT06a: create PMP import file for CA root certificate')
        certificate_file = os.path.abspath('testdata/PAT/06/StartComCa_root.pem')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/06/StartComCa_root.json'))  # output
        cliClient = CliPatool(['-v', 'caCert',
                               '--certfile', certificate_file,
                               '--pvprole', 'IDP',
                               pmpinput_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(pmpinput_file), subdir='PAT/06')

        logging.info('  -- Test PAT06b: create PMP import file for CA intermediate certificate')
        certificate_file = os.path.abspath('testdata/PAT/06/StartComCa_intermed.pem')
        pmpinput_file = os.path.abspath('work/PAT/06/StartComCa_intermed.json')  # output
        cliClient = CliPatool(['-v', 'caCert',
                               '--certfile', certificate_file,
                               '--pvprole', 'IDP',
                               pmpinput_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(pmpinput_file), subdir='PAT/06')


class Test07_adminCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT07: create PMP import file for admin certificate (challenge)')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/07/add_admincert.json'))  # output
        cliClient = CliPatool(['-v', 'adminCert',
                                         '--orgid', '4711',
                                         pmpinput_file])
        PAtool.run_me(cliClient)


if __name__ == '__main__':
    unittest.main()
