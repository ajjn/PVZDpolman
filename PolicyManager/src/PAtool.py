import logging
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
        4) create an EntityDescriptor as a deletion request
        5) create a PMP-input file to revoke a certificate
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
        logging.debug('reading certificate from  ' + self.args.cert.name)
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

        logging.debug('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)
        self.args.output.close()


    def signED(self, projdir_abs):
        ''' Validate XML-Schema and sign with enveloped signature.  '''
        assert self.args.input.name[-4:] == '.xml', 'input file must have the extension .xml'
        ed = SAMLEntityDescriptor(os.path.abspath(self.args.input.name), projdir_abs)
        retmsg = ed.validateXSD()
        if retmsg is not None:
            sys.tracebacklimit = 1
            raise InvalidSamlXmlSchema('File ' +  self.args.input.name + ' is not schema valid:\n' + retmsg)
        unsigned_contents = self.args.input.read()
        md_namespace_prefix = ed.getNamespacePrefix()
        signed_contents = creSignedXML(unsigned_contents,
                                       sigType='enveloped',
                                       sigPosition='/' + md_namespace_prefix + ':EntityDescriptor',
                                       verbose=self.args.verbose)
        if hasattr(self.args, 'signed_output') and self.args.signed_output is not None:
            output_filename = self.args.signed_output
            logging.debug('writing signed document ' + output_filename)
        else:
            output_filename = self.args.input.name[:-4] + '_req.xml'
            logging.debug('writing signed document with default name ' + output_filename)
        with open(output_filename, 'w') as f:
            f.write(signed_contents)
            f.close()


    def deleteED(self):
        logging.debug('creating delete request for entitID ' + self.args.entityid)
        entityDescriptor = '''\
<!-- DELETE entity descriptor from metadata -->
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:pvzd="http://egov.gv.at/pvzd1.xsd"
    pvzd:disposition="delete">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>'''.format(eid=self.args.entityid)
        logging.debug('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)
        self.args.output.close()


    def revokeCert(self):
        logging.debug('reading certificate from ' + self.args.certfile.name)
        x509cert = X509cert(self.args.certfile.read())
        x509cert_pem = x509cert.getPEM_str().replace('\n', '') # JSON string: single line
        pmp_input = '[\n{"record": ["revocation", "%s", "%s"], "delete": false}\n]' % (x509cert_pem, self.args.reason)
        logging.debug('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)
        self.args.output.close()


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
