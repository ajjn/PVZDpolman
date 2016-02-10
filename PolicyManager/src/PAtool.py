import logging, sys, tempfile
from aodsfilehandler import *
from constants import PROJDIR_ABS
from invocation.clipatool import CliPatool
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


    def get_entityid(self, xy509cert) -> str:
        if not (getattr(self.args, 'entityid', False) and getattr(self.args, 'samlrole', False)):
            raise MissingArgumentError('createED requires both entityid and samlrole arguments')
        entityId = self.args.entityid
        #entityId = 'https://' + x509cert.getSubjectCN() + '/' + self.args.samlrole.lower()
        if hasattr(self.args, 'entityid_suffix') and len(self.args.entityid_suffix) > 0:
            if self.args.entityid_suffix[0:1] != '/':
                entityId += '/'
            entityId += self.args.entityid_suffix
        return entityId


    def createED(self):
        logging.debug('reading certificate from ' + self.args.cert.name)
        xy509cert = XY509cert(self.args.cert.read())
        self.args.cert.close()
        entitydescriptor = SAMLEntityDescriptor(createfromcertstr=xy509cert.getPEM_str(),
                                                entityid=self.get_entityid(xy509cert),
                                                samlrole=self.args.samlrole)
        fn = entitydescriptor.get_filename()
        unsigned_basefn = re.sub(r'\.xml$', '.unsigned.xml', fn)
        unsigned_fn = os.path.join(self.args.output_dir, unsigned_basefn)
        logging.debug('writing EntityDescriptor to ' + unsigned_fn)
        with open(unsigned_fn, 'w') as fd:
            fd.write(entitydescriptor.get_xml_str())
        if self.args.sign:
            unsigned_fn = os.path.join(self.args.output_dir, entitydescriptor.get_filename())
            with open(unsigned_xml, 'r') as fd:
                logging.debug('signing ED to ' + self.args.signed_output)
                self.signED(PROJDIR_ABS, fd)


    def signED(self, fn):
        """ Validate XML-Schema and sign with enveloped signature.  """
        with open(fn) as ed_fd:
            ed = SAMLEntityDescriptor(ed_fd)
        ed.validate_xsd()
        unsigned_contents = ed.get_xml_str()
        md_namespace_prefix = ed.get_namespace_prefix()
        signed_contents = creSignedXML(unsigned_contents,
                                       sig_type='enveloped',
                                       sig_position='/' + md_namespace_prefix + ':EntityDescriptor',
                                       verbose=self.args.verbose)
        output_fn = os.path.join(self.args.output_dir, ed.get_filename())
        logging.debug('writing signed EntityDescriptor to ' + output_fn)
        with open(output_fn, 'w') as fd:
            fd.write(signed_contents)


    def deleteED(self):
        logging.debug('creating delete request for entityID ' + self.args.entityid)
        entitydescriptor = SAMLEntityDescriptor(delete_entityid=self.args.entityid)

        unsigned_xml_fn = self.mk_temp_filename() + '.xml'
        logging.debug('writing unsigned ED to ' + unsigned_xml_fn)
        with open(unsigned_xml_fn, 'w') as fd:
            fd.write(entitydescriptor.get_xml_str())
        logging.debug('signing ED to ' + unsigned_xml_fn)
        self.signED(unsigned_xml_fn)
        os.remove(unsigned_xml_fn)


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
        invocation = CliPatool()


    patool = PAtool(invocation.args)
    if (invocation.args.subcommand == 'createED'):
        patool.createED()
    elif (invocation.args.subcommand == 'signED'):
        patool.signED(invocation.args.input_fn)
    #elif (invocation.args.subcommand == 'extractED'):
    #    patool.extractED()
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
