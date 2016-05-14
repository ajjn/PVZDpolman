import logging, sys, tempfile
from aodsfilehandler import *
from constants import PROJDIR_ABS
from invocation.clipatool import CliPatool
from pytool import
from samlentitydescriptor import *
from userexceptions import *
from xmlsigverifyer import XmlSigVerifyer
from xy509cert import XY509cert

__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPatool()


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        print("patool.createED()")
    elif (invocation.args.subcommand == 'signED'):
        print("patool.signED(invocation.args.input_fn)
    elif (invocation.args.subcommand == 'deleteED'):
        print("patool.deleteED()


if __name__ == '__main__':
    run_me()
