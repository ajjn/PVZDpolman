import base64, bz2, sys
import requests
import re
import socket
from constants import DATA_HEADER_B64BZIP
from userExceptions import SecurityLayerUnavailable

__author__ = 'r2h2'

def failIfSecurityLayerUnavailable():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('127.0.0.1', 3495)
    if sock.connect_ex(addr) != 0:
        sys.tracebacklimit = 0
        raise SecurityLayerUnavailable(SecurityLayerUnavailable.__doc__)


def creSignedXML(data, verbose=False):
    ''' compress, b64-encode and sign-envelop the data and return it '''

    failIfSecurityLayerUnavailable()
    dataPacked = DATA_HEADER_B64BZIP + base64.b64encode(bz2.compress(data)).decode('ascii')
    if verbose: print('packed data:\n%s\n' % dataPacked)

    sigRequ = '''\
<?xml version="1.0" encoding="UTF-8"?>
<sl:CreateXMLSignatureRequest
  xmlns:sl="http://www.buergerkarte.at/namespaces/securitylayer/1.2#">
  <sl:KeyboxIdentifier>SecureSignatureKeypair</sl:KeyboxIdentifier>
  <sl:DataObjectInfo Structure="enveloping">
    <sl:DataObject>
      <sl:XMLContent>%s</sl:XMLContent>
    </sl:DataObject>
    <sl:TransformsInfo>
      <sl:FinalDataMetaInfo>
        <sl:MimeType>text/plain</sl:MimeType>
      </sl:FinalDataMetaInfo>
    </sl:TransformsInfo>
  </sl:DataObjectInfo>
</sl:CreateXMLSignatureRequest> ''' % dataPacked

    try:
        r = requests.post('http://localhost:3495/http-security-layer-request',
                          data={'XMLRequest': sigRequ})
    except requests.exceptions.ConnectionError as e:
        print("Cannot connect to security layer (MOCCA) to create a signature " + e.strerror)
        raise
    assert r.text.find('sl:ErrorResponse') < 0, "Security Layer responed with error message."

    # Strip xml root element (CreateXMLSignatureResponse), making disg:Signature the new root:
    # (keeping namespace prefixes - otherwise the signature would break. Therefore not using etree.)
    if verbose: print('security layer create signature response:\n%s\n' % r.text)
    r1 = re.sub(r'<sl:CreateXMLSignatureResponse [^>]*>', '', r.text)
    r2 = re.sub(r'</sl:CreateXMLSignatureResponse>', '', r1)
    return r2


if __name__ == '__main__':
    print(creSignedXML('Testdata'))