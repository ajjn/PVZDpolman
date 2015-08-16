from invocation import *
from aodsListHandler import *
from aodsFileHandler import *
__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        invocation = CliPmpInvocation()
    aodsHandlder = AODSFileHandler(invocation)
    aodsList = AodsList(invocation.args.verbose);
    if (invocation.args.subcommand == 'append'):
        aodsList.aods_append(aodsHandlder,
                         invocation.args.input,
                         xmlsign=invocation.args.xmlsign)
    elif (invocation.args.subcommand == 'create'):
        aodsList.aods_create(aodsHandlder,
                         xmlsign=invocation.args.xmlsign)
    elif (invocation.args.subcommand == 'read'):
        aodsList.aods_read(aodsHandlder,
                       jsondump=invocation.args.jsondump,
                       output=invocation.args.output)
    elif (invocation.args.subcommand == 'scratch'):
        aodsList.aods_scratch(aodsHandlder)

if __name__ == '__main__':
    run_me()
