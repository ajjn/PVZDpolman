from invocation import *
from aodsFileHandler import *
__author__ = 'r2h2'

class PAtool:
    ''' The PAtool (Portaladministrator Tool) performs following functions:
        1) create an EntityDescriptor from a certificate
        2) sign an EntityDescriptor
        3) extract certificate data from metadata
    '''

    def __init__(self, args):
        self.args = args
        #projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        #self.projdir_abs = os.path.abspath(projdir_rel)

    def createED(self):
        pass

    def signED(self):
        assert self.args.input.name[-4:] == '.xml', 'input file must have the extension .xml'
        #with open(self.args.input) as f:
        unsigned_contents = self.args.input.read().encode('utf-8')
        signed_contents = creSignedXML(unsigned_contents, self.args.verbose)
        output_filename = self.args.input.name[-4:] + 'signed.xml'
        with open(output_filename, 'w') as f:
            f.write(signed_contents)

    def extractED(self):
        pass



def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPAtoolInvocation()

    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED()
    elif (invocation.args.subcommand == 'extractED'):
        patool.extractED()


if __name__ == '__main__':
    run_me()
