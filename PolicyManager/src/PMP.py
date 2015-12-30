import logging
from invocation import *
from aodsListHandler import *
from aodsFileHandler import *
__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
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
        except InvalidArgumentValue as e:
            logging.error(e)
    elif (invocation.args.subcommand == 'read'):
        aodsListHandler.aods_read()
    elif (invocation.args.subcommand == 'scratch'):
        aodsListHandler.aods_scratch()

if __name__ == '__main__':
    run_me()
