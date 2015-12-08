from __future__ import print_function
import base64, bz2, datetime, os, re, sys
import simplejson as json
from jnius import autoclass
import xml.etree.ElementTree as ET
from constants import DATA_HEADER_B64BZIP, PROJDIR_ABS
from creSignedXML import creSignedXML
from wrapperRecord import *
from userExceptions import *
__author__ = 'r2h2'


class AODSFileHandler():
    def __init__(self, cliClient):
        self._aodsFile = cliClient.args.aods
        self.verbose = cliClient.args.verbose

        if cliClient.args.xmlsign and self._aodsFile[-4:] != '.xml':
            self._aodsFile += '.xml'
        if not cliClient.args.xmlsign and self._aodsFile[-5:] != '.json':
            self._aodsFile += '.json'
        self.trustCertsFile = os.path.abspath(cliClient.args.trustedcerts)

    def create(self, s, xmlsign):
        if os.path.exists(self._aodsFile):
            raise InvalidArgumentValue('Must remove existing %s before creating a new AODS' % self._aodsFile)
        f = open(self._aodsFile, 'w')
        if xmlsign:
            j = json.dumps(s)
            x = creSignedXML(j, verbose=self.verbose)
            f.write(x)
        else:
            f.write(json.dumps(s))

    def readFile(self):
        if self._aodsFile[-4:] == '.xml':
            # verify xmldsig and extract content
            PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
            verifier = PvzdVerfiySig(
                os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
                os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
                self._aodsFile)
            response  = verifier.verify()
            if response.pvzdCode != 'OK':
                raise ValidationFailure("Signature verification failed, code=" +
                                        response.pvzdCode + "; " + response.pvzdMessage)
            if not os.path.isfile(self.trustCertsFile):
                raise ValidationFailure('Trust certs file not found: %s' % self.trustCertsFile)
            trustCerts = json.loads(open(self.trustCertsFile).read())
            if response.signerCertificateEncoded not in trustCerts:
                raise ValidationFailure("Signature certificate not in trusted list. Signature cert is\n" +
                                        response.signerCertificateEncoded)
            tree = ET.parse(self._aodsFile)
            content = tree.findtext('{http://www.w3.org/2000/09/xmldsig#}Object')
            if len(content) < 0:
                raise ValidationFailure('AODS contained in XML signature value is empty')
            if self.verbose: print('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
            content_body_str = content.replace(DATA_HEADER_B64BZIP, '', 1)
            j_bzip2 = base64.b64decode(content_body_str)
            j = bz2.decompress(j_bzip2)
            return json.loads(j.decode('UTF-8'))
        else:  # must be json
            f = open(self._aodsFile, 'r')
            return json.loads(f.read())

    def removeFile(self):
        ''' remove file but ignore if it does not exist '''
        try:
            os.remove(self._aodsFile)
        except OSError as e:
            if e.errno != 2:
                raise e

    def save(self, s, xmlsign):
        f = open(self._aodsFile, 'w')
        f.truncate()
        if xmlsign:
            f.write(creSignedXML(json.dumps(s)))
        else:
            f.write(json.dumps(s))
