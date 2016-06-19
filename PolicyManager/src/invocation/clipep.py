import argparse, getpass, logging, os, sys
from . import AbstractInvocation
from constants import LOGLEVELS
from userexceptions import *

__author__ = 'r2h2'


class CliPep(AbstractInvocation):
    """ define CLI invocation for PEP.  Test runner can use this by passing testargs """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Enforcement Point')
        self._parser.add_argument('-a', '--aods', dest='aods',
             help='Policy journal (AODS = append only data strcuture)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true",
             help='trace hash chain computation')
        self._parser.add_argument('-l', '--list_trustedcerts', action="store_true",
             help='list trusted vertificates on startup (needs level=DEBUG)')
        self._parser.add_argument('-L', '--loglevel', dest='loglevel_str', choices=LOGLEVELS.keys(),
             help='Level for file logging')
        self._parser.add_argument('-n', '--noxmlsign', action="store_true",
             help='do not sign policy journal with xml signature')
        self._parser.add_argument('-o', '--pepoutdir', dest='pepoutdir',
             help='directory where PEP stores accepted entity descriptors')
        self._parser.add_argument('-r', '--repodir', dest='repodir',
             help='root path of git repo containing the publication request')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts',
             help='file containing json-array of PEM-formatted certificates trusted to sign the policy journal')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")

        if (testargs):
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        self.get_from_env('aods')
        self.get_from_env('pepoutdir')
        self.get_from_env('repodir')
        self.get_from_env('trustedcerts')

        if not hasattr(self.args, 'loglevel_str') or self.args.loglevel_str is None:
            self.args.loglevel_str = 'INFO'
        if 'PEPLOGLEVEL' in os.environ:
            self.args.loglevel_str = os.environ['PEPLOGLEVEL']
        self.args.loglevel = LOGLEVELS[self.args.loglevel_str]


    def get_from_env(self, argname):
        if not getattr(self.args, argname, False):
            env_name = 'POLMAN_%s' % argname.upper()
            if env_name in os.environ:
                setattr(self.args, argname, os.environ[env_name])
            else:
                raise InvalidArgumentValueError('neither --%s nor %s provided' % (argname, env_name))
