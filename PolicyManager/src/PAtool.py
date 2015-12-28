from invocation import *
from aodsFileHandler import *
from SAMLEntityDescriptor import *
from userExceptions import *
from x509cert import X509cert

__author__ = 'r2h2'

class PAtool:
    ''' The PAtool (Portaladministrator Tool) performs following functions:
        1) create an EntityDescriptor from a certificate
        2) sign an EntityDescriptor
        3) extract certificate data from metadata
        4) create an EntityDescriptor to revoke a certificate
    '''

    def __init__(self, args):
        self.args = args

    #def extractX509SubjectCN(self) -> str:
    #    pass # TODO implement

    def getEntityId(self,x509cert) -> str:
        entityId = self.args.entityid + '/' + self.args.samlrole.lower()
        #entityId = 'https://' + x509cert.getSubjectCN() + '/' + self.args.samlrole.lower()
        if hasattr(self.args, 'entityid_suffix') and len(self.args.entityid_suffix) > 0:
            if self.args.entityid_suffix[0:1] != '/':
                entityId += '/'
            entityId += self.args.entityid_suffix
        return entityId


    def createED(self):
        if self.args.verbose: print('reading certificate from  ' + self.args.cert.name)
        x509cert = X509cert(self.args.cert.read())
        entityId = self.getEntityId(x509cert)
        if self.args.samlrole == 'IDP':
            entityDescriptor = '''\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>'''.format(eid=entityId, pem=x509cert.getPEM_str())
        elif self.args.samlrole == 'SP':
            entityDescriptor = '''\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
      <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/acs/unused" index="0" isDefault="true"/>
    </md:KeyDescriptor>
  </md:SPSSODescriptor>
</md:EntityDescriptor>'''.format(eid=entityId, pem=x509cert.getPEM_str())
        else:
            raise EntityRoleNotSupported("Only IDP and SP entity roles implemented, but %s given" % self.args.samlrole)

        if self.args.verbose: print('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)

    def signED(self, projdir_abs):
        assert self.args.input.name[-4:] == '.xml', 'input file must have the extension .xml'
        ed = SAMLEntityDescriptor(os.path.abspath(self.args.input.name), projdir_abs)
        retmsg = ed.validateXSD()
        if retmsg is not None:
            sys.tracebacklimit = 1
            raise InvalidSamlXmlSchema('File ' +  self.args.input.name + ' is not schema valid:\n' + retmsg)
        unsigned_contents = self.args.input.read()
        signed_contents = creSignedXML(unsigned_contents, verbose=self.args.verbose)
        if hasattr(self.args, 'signed_output') and self.args.signed_output is not None:
            output_filename = self.args.signed_output
            if self.args.verbose: print('writing signed document ' + output_filename)
        else:
            output_filename = self.args.input.name[:-4] + '_req.xml'
            if self.args.verbose: print('writing signed document with default name ' + output_filename)
        with open(output_filename, 'w') as f:
            f.write(signed_contents)

    def extractED(self):
        pass  # TODO implement

    def deleteED(self):
        if self.args.verbose: print('reading certificate from  ' + self.args.cert.name)
        x509cert = X509cert(self.args.cert.read())
        entityId = self.getEntityId(x509cert)
        entityDescriptor = '''\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:pvzd="http://egov.gv.at/pvzd1.xsd"
    pvzd:disposition="delete">  <!-- delete entity descriptor from metadata -->
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>'''.format(eid=entityId, pem=x509cert.getPEM_str())
        if self.args.verbose: print('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)

    def revokeCert(self):
        if self.args.verbose: print('reading certificate from ' + self.args.cert.name)
        x509cert = X509cert(self.args.cert.read())
        pmp_input = '[{"record": ["revocation", "{cert}%s"], "delete": false}]' % x509cert.getPEM_str()
        if self.args.verbose: print('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)


def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPAtoolInvocation()
    projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    projdir_abs = os.path.abspath(projdir_rel)


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED(projdir_abs)
    elif (invocation.args.subcommand == 'extractED'):
        patool.extractED()
    elif (invocation.args.subcommand == 'deleteED'):
        patool.deleteED()
    elif (invocation.args.subcommand == 'revokeCert'):
        patool.revokeCert()


if __name__ == '__main__':
    run_me()
