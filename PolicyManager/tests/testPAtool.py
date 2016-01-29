import difflib, os, sys
import unittest
from assertNoDiff import assertNoDiff
from invocation import CliPAtoolInvocation
import PAtool
from userexceptions import *

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


class Test01_createED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT01: create EntitDescriptor from certificate (pvzd:pvptype="R-Profile")')
        certificate_file = os.path.abspath('testdata/redmineIdentineticsCom-cer.pem')
        entitydescriptor_file = os.path.abspath('work/PAT02_redmineIdentineticsOrg_ed.xml')
        cliClient = CliPAtoolInvocation(['-v', '-r', 'IDP',
                                         '-e', 'https://redmine.identinetics.com',
                                         'createED',
                                         certificate_file,
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(entitydescriptor_file))


class Test02_signED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT02a: sign EntityDescriptor w/o xml header to default output')
        entitydescriptor_file = os.path.abspath('work/PAT02_redmineIdentineticsOrg_ed.xml')
        cliClient = CliPAtoolInvocation(['-v', 'signED',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)

        logging.info('  -- Test PAT02b: sign EntityDescriptor with xml header to specified output')
        entitydescriptor_file = os.path.abspath('testdata/PAT02_idpExampleCom.xml')
        entitydescriptor_sig_file = os.path.abspath('work/PAT02_idpExampleCom_sig.xml')
        cliClient = CliPAtoolInvocation(['-v', '-s', entitydescriptor_sig_file,
                                         'signED',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)
        # skipping comparison with ref data: signatures are time-stamped, would need xpath filter ..

class Test03_signED_invalidXSD(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT03: sign EntityDescriptor with invalid SAML schema (OK with xmllint, failing with xerces)')
        entitydescriptor_file = os.path.abspath('testdata/PEP02_gondorMagwienGvAt_ed_invalid_xsd.xml')
        cliClient = CliPAtoolInvocation(['-v', 'signED',
                                         entitydescriptor_file])
        with self.assertRaises(InvalidSamlXmlSchemaError) as context:
            PAtool.run_me(cliClient)


class Test04_deleteED(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT04: create request to delete EntityDescriptor from metadata')
        entitydescriptor_file = os.path.abspath('work/PAT04_redmineIdentineticsOrg_ed_delete.xml')
        cliClient = CliPAtoolInvocation(['-v', '--entityid', 'https://redmine.identinetics.com',
                                         'deleteED',
                                         entitydescriptor_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(entitydescriptor_file))


class Test05_revokeCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT05: create PMP import file to revoke a certificate')
        certificate_file = os.path.abspath('testdata/PAT05_gondorMagwienGvAt_2011-cer.pem')
        pmpinput_file = os.path.abspath('work/PAT05_gondorMagwienGvAt_2011-cer_revoke.json')  # output
        pmpref_file = os.path.abspath('testdata/PAT05_gondorMagwienGvAt_2011-cer_revoke.json')
        cliClient = CliPAtoolInvocation(['-v', '--certfile', certificate_file,
                                         'revokeCert',
                                         '--reason', 'testing revocation',
                                         pmpinput_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(pmpinput_file))


class Test06_caCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT06: create PMP import file for CA certificate')
        certificate_file = os.path.abspath('testdata/PAT06_StartComCa_root.pem')
        pmpinput_file = os.path.abspath('work/PAT06_StartComCa_root.json')  # output
        pmpref_file = os.path.abspath('testdata/PAT06_StartComCa_root.json')
        cliClient = CliPAtoolInvocation(['-v', '--certfile', certificate_file,
                                         'caCert',
                                         '--pvprole', 'IDP',
                                         pmpinput_file])
        PAtool.run_me(cliClient)
        assertNoDiff(os.path.basename(pmpinput_file))


if __name__ == '__main__':
    unittest.main()
