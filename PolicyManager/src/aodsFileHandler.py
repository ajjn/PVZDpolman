from __future__ import print_function
import base64, bz2, datetime, os, re, sys
import simplejson as json
from jnius import autoclass
import xml.etree.ElementTree as ET
from wrapperRecord import *
from userExceptions import *
from creSignedXML import creSignedXML
from constants import PROJDIR_ABS
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
            print('Must remove existing %s before creating a new AODS' % self._aodsFile)
            sys.exit(1)
        f = open(self._aodsFile, 'w')
        if xmlsign:
            j = json.dumps(s)
            x = creSignedXML(j, verbose=self.verbose)
            f.write(x.encode("utf-8"))
        else:
            f.write(json.dumps(s))

    def readFile(self):
        if self._aodsFile[-4:] == '.xml':
            # verify xmldsig and extract content
            PvzdVerfiySig = autoclass('PvzdVerifySig')
            verifier = PvzdVerfiySig(
                os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
                os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
                self._aodsFile)
            response  = verifier.verify()
            assert 'OK' == response.pvzdCode, \
                "Signature verification failed, code=" + response.pvzdCode + "; " + response.pvzdMessage
            assert os.path.isfile(self.trustCertsFile), \
                'Trust certs file not found: %s' % self.trustCertsFile
            trustCerts = json.loads(open(self.trustCertsFile).read())
            assert response.signerCertificateEncoded in trustCerts, \
                "Signature certificate not in trusted list. Signature cert is\n" + response.signerCertificateEncoded
            tree = ET.parse(self._aodsFile)
            content = tree.findtext('{http://www.w3.org/2000/09/xmldsig#}Object')
            assert len(content) > 0, 'AODS contained in XML signature value is empty'
            if self.verbose: print('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
            content_body = re.sub(DATA_HEADER_B64BZIP, '', content)
            j = bz2.decompress(base64.b64decode(content_body))
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
