from invocation import *
from aods import *


__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        invocation = CLIInvocation()
    aodsHandlder = AODSFileHandler(invocation)
    aods = AODS(invocation.args.verbose);
    if (invocation.args.subcommand == 'append'):
        aods.aods_append(aodsHandlder,
                         invocation.args.input,
                         trustedcerts=invocation.args.trustedcerts,
                         xmlsign=invocation.args.xmlsign)
    elif (invocation.args.subcommand == 'create'):
        aods.aods_create(aodsHandlder,
                         xmlsign=invocation.args.xmlsign)
    elif (invocation.args.subcommand == 'read'):
        aods.aods_read(aodsHandlder,
                       trustedcerts=invocation.args.trustedcerts,
                       jsondump=invocation.args.jsondump,
                       output=invocation.args.output)
    elif (invocation.args.subcommand == 'scratch'):
        aods.aods_scratch(aodsHandlder)

if __name__ == '__main__':
    run_me()
