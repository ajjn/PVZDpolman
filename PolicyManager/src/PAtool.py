import logging, tempfile
from aodsfilehandler import *
from constants import PROJDIR_ABS
from invocation import *
from samlentitydescriptor import *
from userexceptions import *
from xmlsigverifyer import XmlSigVerifyer
from xy509cert import XY509cert

__author__ = 'r2h2'

class PAtool:
    """ The PAtool (Portaladministrator Tool) performs following functions:
        1) create an EntityDescriptor from a certificate
        2) sign an EntityDescriptor
        3) extract certificate data from metadata
        4) create an EntityDescriptor as a deletion request
        5) create a PMP-input file to revoke a certificate
        6) create a PMP-input file to import a CA certificate
    """

    def __init__(self, args):
        self.args = args


    #def extractX509SubjectCN(self) -> str:
    #    pass # TODO implement


    def get_entityid(self, x509cert) -> str:
        if not (getattr(self.args, 'entityid', False) and getattr(self.args, 'samlrole', False)):
            raise MissingArgumentError('createED requires both entityid and samlrole arguments')
        entityId = self.args.entityid + '/' + self.args.samlrole.lower()
        #entityId = 'https://' + x509cert.getSubjectCN() + '/' + self.args.samlrole.lower()
        if hasattr(self.args, 'entityid_suffix') and len(self.args.entityid_suffix) > 0:
            if self.args.entityid_suffix[0:1] != '/':
                entityId += '/'
            entityId += self.args.entityid_suffix
        return entityId


    def createED(self):
        logging.debug('reading certificate from ' + self.args.cert.name)
        x509cert = XY509cert(self.args.cert.read())
        self.args.cert.close()
        entityId = self.get_entityid(x509cert)
        if self.args.samlrole == 'IDP':
            entityDescriptor = """\
<md:EntityDescriptor entityID="{eid}" pvzd:pvptype="R-Profile" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:pvzd="http://egov.gv.at/pvzd1.xsd">
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
</md:EntityDescriptor>""".format(eid=entityId, pem=x509cert.getPEM_str())
        elif self.args.samlrole == 'SP':
            entityDescriptor = """\
<md:EntityDescriptor entityID="{eid}" pvzd:pvptype="R-Profile" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:pvzd="http://egov.gv.at/pvzd1.xsd">
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
</md:EntityDescriptor>""".format(eid=entityId, pem=x509cert.getPEM_str())
        else:
            raise EntityRoleNotSupportedError("Only IDP and SP entity roles implemented, but %s given" % self.args.samlrole)

        logging.debug('writing ED to ' + self.args.output.name)
        self.args.output.write(entityDescriptor)
        self.args.output.close()


    def signED(self, projdir_abs, ed_fd):
        """ Validate XML-Schema and sign with enveloped signature.  """
        ed = SAMLEntityDescriptor(ed_fd)
        ed.validate_xsd()
        unsigned_contents = ed_fd.read()
        md_namespace_prefix = ed.get_namespace_prefix()
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


    def deleteED(self):
        logging.debug('creating delete request for entityID ' + self.args.entityid)
        entityDescriptor = """\
<!-- DELETE entity descriptor from metadata -->
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:pvzd="http://egov.gv.at/pvzd1.xsd"
    pvzd:disposition="delete">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>""".format(eid=self.args.entityid)
        unsigned_xml = self.mk_temp_filename() + '.xml'
        logging.debug('writing unsigned ED to ' + unsigned_xml)
        with open(unsigned_xml, 'w') as fd:
            fd.write(entityDescriptor)
        with open(unsigned_xml, 'r') as fd:
            logging.debug('signing ED to ' + self.args.signed_output)
            self.signED(PROJDIR_ABS, fd)
        os.remove(unsigned_xml)


    def revokeCert(self):
        logging.debug('reading certificate from ' + self.args.certfile.name)
        x509cert = XY509cert(self.args.certfile.read())
        self.args.certfile.close()
        x509cert_pem = x509cert.getPEM_str().replace('\n', '') # JSON string: single line
        pmp_input = '[\n{"record": ["revocation", "%s", "%s"], "delete": false}\n]' % \
                    (x509cert_pem, self.args.reason)
        logging.debug('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)
        self.args.output.close()


    def caCert(self):
        logging.debug('reading ca certificate from ' + self.args.certfile.name)
        x509cert = XY509cert(self.args.certfile.read())
        self.args.certfile.close()
        x509cert_pem = x509cert.getPEM_str().replace('\n', '') # JSON string: single line
        pmp_input = '[\n{"record": ["issuer", "%s", "%s", "%s"], "delete": false}\n]' % \
                    (x509cert.getSubjectCN(), self.args.pvprole, x509cert_pem)
        logging.debug('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)
        self.args.output.close()


    def mk_temp_filename(self) -> str:
        """ temp file name method that should work on both POSIX & Win"""
        (fd, filename) = tempfile.mkstemp()
        os.close(fd)
        os.remove(filename)
        return filename

    def adminCert(self):
        logging.debug('challenging admin to create a signature to extract signing cert')
        x = creSignedXML('sign this dummy text - result is used to extract signature certificate.')
        fn = self.mk_temp_filename() + '.xml'
        with open(fn, 'w') as f:
            f.write(x)
        xml_sig_verifyer = XmlSigVerifyer();
        signerCertificateEncoded = xml_sig_verifyer.verify(fn, verify_file_extension=False)
        x509cert = XY509cert('-----BEGIN CERTIFICATE-----\n' + \
             signerCertificateEncoded + \
             '\n-----END CERTIFICATE-----\n')
        x509cert_pem = x509cert.getPEM_str().replace('\n', '') # JSON string: single line
        pmp_input = '[\n{"record": ["userprivilege", "{cert}%s", "%s", "%s"], "delete": false}\n]' % \
                    (x509cert_pem, self.args.orgid, x509cert.getSubjectCN())
        logging.debug('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)
        self.args.output.close()


def run_me(testrunnerInvocation=None):
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPAtoolInvocation()


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED(PROJDIR_ABS, invocation.args.input)
        invocation.args.input.close()
    elif (invocation.args.subcommand == 'extractED'):
        patool.extractED()
    elif (invocation.args.subcommand == 'deleteED'):
        patool.deleteED()
    elif (invocation.args.subcommand == 'revokeCert'):
        patool.revokeCert()
    elif (invocation.args.subcommand == 'caCert'):
        patool.caCert()
    elif (invocation.args.subcommand == 'adminCert'):
        patool.adminCert()


if __name__ == '__main__':
    run_me()
