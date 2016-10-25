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



class Test08_adminCert(unittest.TestCase):
    def runTest(self):
        logging.info('  -- Test PAT08a: create PMP import file for admin certificate (import)')
        certificate_file = os.path.abspath('testdata/PAT/08/ecard_qcert.pem')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/08/add_admincert-a.json'))  # output
        cliClient = CliPatool(['-v', 'adminCert',
                               '--orgid', 'L10',
                               '--certfile', certificate_file,
                               pmpinput_file])
        PAtool.run_me(cliClient)


        logging.info('  -- Test PAT08b: create PMP import file for admin certificate (import)')
        certificate_file = os.path.abspath('testdata/PAT/08/ecard_qcert_multiline.b64')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/08/add_admincert-b.json'))  # output
        cliClient = CliPatool(['-v', 'adminCert',
                               '--orgid', 'L10',
                               '--certfile', certificate_file,
                               pmpinput_file])
        PAtool.run_me(cliClient)


        logging.info('  -- Test PAT08c: create PMP import file for admin certificate (import)')
        certificate_file = os.path.abspath('testdata/PAT/08/ecard_qcert_multiline.b64')
        pmpinput_file = make_dirs(os.path.abspath('work/PAT/08/add_admincert-c.json'))  # output
        cliClient = CliPatool(['-v', 'adminCert',
                               '--orgid', 'L10',
                               '--certfile', certificate_file,
                               pmpinput_file])
        PAtool.run_me(cliClient)

if __name__ == '__main__':
    unittest.main()
