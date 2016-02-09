import argparse, getpass, sys
from . import AbstractInvocation
from constants import LOGLEVELS
from userexceptions import *

__author__ = 'r2h2'


class CliPep(AbstractInvocation):
    """ define CLI invocation for PEP.  Test runner can use this by passing testargs """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Enforcement Point')
        self._parser.add_argument('-a', '--aods', dest='aods', required=True,
             help='Policy journal (AODS = append only data strcuture)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true",
             help='trace hash chain computation')
        self._parser.add_argument('-l', '--list_trustedcerts', action="store_true",
             help='list trusted vertificates on startup (needs level=DEBUG)')
        self._parser.add_argument('-L', '--loglevel', dest='loglevel_str', choices=LOGLEVELS.keys(),
             help='Level for file logging')
        self._parser.add_argument('-o', '--pepoutdir', dest='pepoutdir', required=True,
             help='directory where PEP stores accepted entity descriptors')
        self._parser.add_argument('-r', '--pubrequ', dest='pubrequ', default='.',
             help='root path of git repo containing the publication request')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts', default='trustedcerts.json',
             help='file containing json-array of PEM-formatted certificates trusted to sign the policy journal')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-x', '--xmlsign', action="store_true",
             help='use signed xml format for policy journal)')

        if (testargs):
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if not hasattr(self.args, 'loglevel_str') or self.args.loglevel_str is None:
            self.args.loglevel_str = 'INFO'
        self.args.loglevel = LOGLEVELS[self.args.loglevel_str]
