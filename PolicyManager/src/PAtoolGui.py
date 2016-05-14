import logging, sys, tempfile
from invocation.guipatool import GuiPatool
from PAtool import PAtool

__author__ = 'r2h2'


def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"

    invocation = GuiPatool()


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED(invocation.args.input_fn)
    elif (invocation.args.subcommand == 'deleteED'):
        patool.deleteED()

    #if (invocation.args.subcommand == 'createED'):
    #    print("patool.createED()")
    #elif (invocation.args.subcommand == 'signED'):
    #    print("patool.signED(invocation.args.input_fn)")
    #elif (invocation.args.subcommand == 'deleteED'):
    #    print("patool.deleteED()")


if __name__ == '__main__':
    run_me()
