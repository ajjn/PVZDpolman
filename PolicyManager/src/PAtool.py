# STUB version of PATool for simlified development
import sys
#from constants import PROJDIR_ABS
from invocation.clipatool import CliPatool
from samlentitydescriptor import *
from userexceptions import *

__author__ = 'r2h2'

class PAtool:
    """ The PAtool (Portaladministrator Tool) performs following functions:
        1) create an EntityDescriptor from a certificate
        2) sign an EntityDescriptor
        3) extract certificate data from metadata
    """

    def __init__(self, args):
        self.args = args


    def get_entityid(self) -> str:
        return "https://dummy.entityid.test/xx"


    def createED(self):
        print('reading certificate from ' + self.args.cert.name)
        self.args.cert.close()
        entitydescriptor = SAMLEntityDescriptor(createfromcertstr="dummypemstringfortest",
                                                entityid=self.get_entityid(),
                                                samlrole=self.args.samlrole)
        fn = entitydescriptor.get_filename()
        unsigned_basefn = re.sub(r'\.xml$', '.unsigned.xml', fn)
        unsigned_fn = os.path.abspath(os.path.join(self.args.output_dir, unsigned_basefn))
        print('writing EntityDescriptor to ' + unsigned_fn)
        with open(unsigned_fn, 'w') as fd:
            fd.write(entitydescriptor.get_xml_str())
        if self.args.sign:
            print('signing ED')
            self.signED(unsigned_fn)


    def signED(self, fn):
        """ Validate XML-Schema and sign with enveloped signature.  """
        with open(fn) as ed_fd:
            ed = SAMLEntityDescriptor(ed_fd)
        signed_contents = ed.get_xml_str()
        output_fn = os.path.join(self.args.output_dir, ed.get_filename())
        print('writing signed EntityDescriptor to ' + output_fn)
        with open(output_fn, 'w') as fd:
            fd.write(signed_contents)


    def deleteED(self):
        print('creating delete request for entityID ' + self.args.entityid)
        entitydescriptor = SAMLEntityDescriptor(delete_entityid=self.args.entityid)
        fn = entitydescriptor.get_filename()
        print('writing signed EntityDescriptor to ' + fn)
        with open(fn, 'w') as fd:
            fd.write(entitydescriptor.get_xml_str())




def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    invocation = guiPatool()


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED(invocation.args.input_fn)
    elif (invocation.args.subcommand == 'deleteED'):
        patool.deleteED()


if __name__ == '__main__':
    run_me()
