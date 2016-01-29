import logging
from invocation import *
from aodslisthandler import *
from aodsfilehandler import *
__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        invocation = CliPmpInvocation()

    aodsFileHandlder = AODSFileHandler(invocation)
    aodsListHandler = AodsListHandler(aodsFileHandlder, invocation.args)

    if (invocation.args.subcommand == 'append'):
        aodsListHandler.aods_append()
    elif (invocation.args.subcommand == 'create'):
        try:
            aodsListHandler.aods_create()
        except InvalidArgumentValueError as e:
            logging.error(e)
    elif (invocation.args.subcommand == 'read'):
        aodsListHandler.aods_read()
    elif (invocation.args.subcommand == 'scratch'):
        aodsListHandler.aods_scratch()

if __name__ == '__main__':
    run_me()
