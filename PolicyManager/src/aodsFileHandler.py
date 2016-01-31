import base64, bz2, datetime, os, re, sys
import logging
import simplejson as json
import xml.etree.ElementTree as ET
from constants import DATA_HEADER_B64BZIP
from cresignedxml import creSignedXML
from wrapperrecord import *
from userexceptions import EmptyAODSError, InvalidArgumentValueError, ValidationError
from xmlsigverifyer import XmlSigVerifyer
from xy509cert import XY509cert
__author__ = 'r2h2'


class AODSFileHandler():
    def __init__(self, cliClient):
        self._aodsFile = cliClient.args.aods
        self.verbose = cliClient.args.verbose
        self.list_trustedcerts = cliClient.args.list_trustedcerts

        if cliClient.args.xmlsign and self._aodsFile[-4:] != '.xml':
            self._aodsFile += '.xml'
        if not cliClient.args.xmlsign and self._aodsFile[-5:] != '.json':
            self._aodsFile += '.json'
        self.trustCertsFile = os.path.abspath(cliClient.args.trustedcerts)

    def do_list_trustedcerts(self, trustCerts, signerCertificateEncoded):
        for cert in trustCerts:
            logging.debug('--- List of  certificates trusted to sign the policy journal. '
                         'Certificate for current journal is marked with ">>".')
            linemarker = ('>>' if cert == signerCertificateEncoded else '')
            xy509cert = XY509cert(cert, 'PEM')
            logging.debug(linemarker + 's: ' + xy509cert.getSubject_str() +
                         ', i:' + xy509cert.getIssuer_str() +
                         'not after: ' + xy509cert.notValidAfter())
        logging.debug('--- End of list of trusted certificates.')

    def create(self, s, xmlsign):
        if os.path.exists(self._aodsFile):
            raise InvalidArgumentValueError('Must remove existing %s before creating a new AODS' %
                                            self._aodsFile)
        if xmlsign:
            j = json.dumps(s)
            x = creSignedXML(j, verbose=self.verbose)
            with open(self._aodsFile, 'w') as f:
                f.write(x)
        else:
            with open(self._aodsFile, 'w') as f:
                f.write(json.dumps(s))

    def readFile(self):
        if self._aodsFile[-4:] == '.xml':
            # verify whether the signature is valid
            xml_sig_verifyer = XmlSigVerifyer();
            signerCertificateEncoded = xml_sig_verifyer.verify(self._aodsFile)
            # verify whether the signer is authorized
            if not os.path.isfile(self.trustCertsFile):
                raise ValidationError('Trust certs file not found: %s' % self.trustCertsFile)
            with open(self.trustCertsFile) as f:
                trustCerts = json.loads(f.read())
            if signerCertificateEncoded not in trustCerts:
                raise ValidationError("Signature certificate not in trusted list. "
                                      "Signature cert is\n" + signerCertificateEncoded)
            if self.list_trustedcerts:
                self.do_list_trustedcerts(trustCerts, signerCertificateEncoded)
            # get contents
            tree = ET.parse(self._aodsFile)
            content = tree.findtext('{http://www.w3.org/2000/09/xmldsig#}Object')
            if len(content) < 0:
                raise ValidationError('AODS contained in XML signature value is empty')
            # logging.debug('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
            content_body_str = content.replace(DATA_HEADER_B64BZIP, '', 1)
            j_bzip2 = base64.b64decode(content_body_str)
            j = bz2.decompress(j_bzip2)
            return json.loads(j.decode('UTF-8'))
        else:  # must be json
            with open(self._aodsFile, 'r') as f:
                j = json.loads(f.read())
            return j

    def removeFile(self):
        ''' remove file but ignore if it does not exist '''
        try:
            os.remove(self._aodsFile)
        except OSError as e:
            if e.errno != 2:
                raise e

    def save(self, s, xmlsign):
        if xmlsign:
            xml = creSignedXML(json.dumps(s))
            if len(xml) == 0:  # just for defense, should not happen
                raise EmptyAODSError('Journal empty, not saved - signature failed?')
            with open(self._aodsFile, 'w') as f:
                f.truncate()
                f.write(xml)
        else:
            with open(self._aodsFile, 'w') as f:
                f.truncate()
                f.write(json.dumps(s))
