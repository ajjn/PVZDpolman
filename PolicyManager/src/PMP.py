import logging
import logging.config
import os
from aodslisthandler import *
from aodsfilehandler import *
from constants import LOGLEVELS
from invocation.clipmp import CliPmp
import loggingconfig


__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
        if 'LOGLEVEL' in os.environ and os.path.isfile(os.environ['LOGLEVEL']):
            loglevel = os.environ['LOGLEVEL']
        else:
            loglevel = 'INFO'
        logging_config = loggingconfig.LoggingConfig(logbasename,
                                                     console=True,
                                                     file_level=loglevel)
        exception_lvl = LOGLEVELS['ERROR']
        logging.debug('logging level=' + loglevel)
        invocation = CliPmp()
        for opt in [a for a in dir(invocation.args) if not a.startswith('_')]:
            #print(opt + '=' + str(getattr(invocation.args, opt)))
            logging.debug(opt + '=' + str(getattr(invocation.args, opt)))

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
