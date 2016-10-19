import base64
import logging
import lxml.etree
import re
import sys
#import signxml
import tempfile

from aodsfilehandler import *
from constants import PROJDIR_ABS, XMLNS_DSIG, XMLNS_MD
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
        if not os.path.isdir(self.args.output_dir):
            raise InvalidArgumentValueError('output dir must be an existing directory: ' +
                                            self.args.output_dir)
        unsigned_fn = os.path.join(self.args.output_dir, unsigned_basefn)
        logging.debug('writing EntityDescriptor to ' + unsigned_fn)
        with open(unsigned_fn, 'w') as fd:
            fd.write(entitydescriptor.get_xml_str())
        if self.args.sign:
            logging.debug('signing ED')
            self.signED(unsigned_fn)


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

    def adminCertSignChallenge(self) -> str:
        logging.debug('challenging admin to create a signature to extract signing cert')
        x = creSignedXML('sign this dummy text - result is used to extract signature certificate.')
        fn = self.mk_temp_filename() + '.xml'
        with open(fn, 'w') as f:
            f.write(x)
        xml_sig_verifyer = XmlSigVerifyer();
        xml_sig_verifyer_response = xml_sig_verifyer.verify(fn, verify_file_extension=False)
        return XY509cert('-----BEGIN CERTIFICATE-----\n' + \
                         xml_sig_verifyer_response.signer_cert_pem + \
                         '\n-----END CERTIFICATE-----\n')

    def adminCertFromFile(self) -> str:
        filecontent = self.args.certfile.read()
        self.args.certfile.close()
        if filecontent.startswith('-----BEGIN CERTIFICATE-----\n'):
            return filecontent
        else:
            return '-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----\n' % filecontent

    def adminCert(self):
        if 'certfile' in self.args and self.args.certfile is not None:
            x509cert_pem_multiline = self.adminCertFromFile()
        else:
            x509cert_pem_multiline = self.adminCertSignChallenge().cert_str
        x509cert = XY509cert(x509cert_pem_multiline)
        x509cert_pem_singleline = x509cert_pem_multiline.replace('\n', '')  # JSON string must be a single line
        pmp_input = '[\n{"record": ["userprivilege", "{cert}%s", "%s", "%s"], "delete": false}\n]' % \
                    (x509cert_pem_singleline, self.args.orgid, x509cert.getSubjectCN())
        logging.debug('writing PMP input file to ' + self.args.output.name)
        self.args.output.write(pmp_input)
        self.args.output.close()

    def export_certs_idp(self):
        #logging.debug('validating metadata signature')
        #with open(self.args.md_cert, 'r') as fd:
        #    md_cert_pem = fd.read()
        #md_dom = lxml.etree.parse(self.args.metadata)
        #asserted_metadata = signxml.xmldsig(md_dom.getroot()).verify(x509_cert=md_cert_pem)
        # TODO: implement signature validation (xmlsectool, signxml)
        asserted_metadata = lxml.etree.parse(self.args.metadata)

        logging.debug('exporting IDP certs from metadata')
        md_root = lxml.etree.fromstring(asserted_metadata).getroot()
        print('EntityID | Subject | Issuer | Serial | Not valid after')
        for e in md_root.findall(XMLNS_MD + 'EntityDescriptor'):
            ed = SAMLEntityDescriptor(ed_bytes=lxml.etree.tostring(e).decode('utf-8'))
            xy509certs = ed.get_signing_certs(samlrole='IDP')
            outputdir = os.path.abspath(self.args.output_dir)
            os.makedirs(outputdir, exist_ok=True)
            i = 1
            for xy509cert in xy509certs:
                fname = re.sub(r'\.xml$', '', ed.get_filename()) + ('_idp_crt_%s.pem' % str(i))
                if xy509cert.getIssuer_str() == xy509cert.getSubject_str():
                    issuer = '//self-signed//'
                else:
                    issuer = xy509cert.getIssuer_str()
                with open(os.path.join(outputdir, fname), 'w') as fd:
                    fd.write('signing cert for IDP of entity ' + ed.get_entityid() + '\n')
                    fd.write('subject: ' + xy509cert.getSubject_str() + '\n')
                    fd.write('issuer: ' + issuer + '\n')
                    fd.write('serial (hex): ' + xy509cert.get_serial_number_hex() + '\n')
                    fd.write('serial (int): ' + str(xy509cert.get_serial_number_int()) + '\n')
                    fd.write('notValidAfter: ' + xy509cert.notValidAfter(formatted=True) + '\n')
                    fd.write('fingerfd.write (SHA1): ' + xy509cert.digest() + '\n')
                    fd.write('fingerfd.write (MD5): ' + xy509cert.digest(dgst='MD5') + '\n')
                    fd.write(xy509cert.pem_add_rfc7468_delimiters(xy509cert.cert_str) + '\n')
                print(ed.get_entityid()  + ' | ' +
                      xy509cert.getSubject_str() + ' | ' +
                      issuer + ' | ' +
                      xy509cert.get_serial_number_hex() + ' | ' +
                      xy509cert.notValidAfter(formatted=True)
                     )
                i += 1


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
    elif (invocation.args.subcommand == 'exportCerts'):
        patool.export_certs_idp()


if __name__ == '__main__':
    run_me()
