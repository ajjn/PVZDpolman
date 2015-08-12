from __future__ import print_function
import base64, bz2
import requests
import re

__author__ = 'r2h2'


def creSignedXML(data, verbose=False):
    ''' compress, b64-encode and sign-envelop the data and return it '''

    dataPacked = base64.b64encode(bz2.compress(data))
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
    except requests.exceptions.ConnectionError, e:
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
