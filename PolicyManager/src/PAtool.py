from invocation import *
from aodsFileHandler import *
from x509cert import X509cert
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

    def extractX509SubjectCN(self) -> str:
        pass #TODO implement

    def getEntityId(self,x509cert) -> str:
        entityId = 'https://' + x509cert.getSubjectCN() + '/' + self.args.samlrole.lower()
        if hasattr(self.args, 'entityid_suffix') and len(self.args.entityid_suffix) > 0:
            if self.args.entityid_suffix[0:1] != '/':
                entityId += '/'
            entityId += self.args.entityid_suffix
        return entityId


    def createED(self):
        if self.args.verbose: print('reading certificate from  ' + self.args.cert.name)
        x509cert = X509cert(self.args.cert.read())
        entityId = self.getEntityId(x509cert)
        entityDescriptor = '''\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <md{samlrole}SSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
  </md:{samlrole}SSODescriptor>
</md:EntityDescriptor>'''.format(eid=entityId, pem=x509cert.getPEM_str(), samlrole=self.args.samlrole)
        if self.args.verbose: print('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)


    def signED(self):
        assert self.args.input.name[-4:] == '.xml', 'input file must have the extension .xml'
        unsigned_contents = self.args.input.read()
        signed_contents = creSignedXML(unsigned_contents, self.args.verbose)
        if hasattr(self.args, 'signed_output'):
            output_filename = self.args.signed_output
            if self.args.verbose: print('writing signed document ' + output_filename)
        else:
            output_filename = self.args.input.name[:-4] + '_signed.xml'
            if self.args.verbose: print('writing signed document with default name ' + output_filename)
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
