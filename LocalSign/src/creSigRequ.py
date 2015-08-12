from __future__ import print_function
import base64, bz2
import requests

__author__ = 'r2h2'


def creSigRequ(data, verbose=False):
    ''' compress, b64-encode and sign-envelop the data and return it '''

    dataPacked = base64.b64encode(bz2.compress(data))
    if verbose: print('\n%s\n' % dataPacked)

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

    r = requests.post('http://localhost:3495/http-security-layer-request',
                      data={'XMLRequest': sigRequ})
    return r.text


if __name__ == '__main__':
    print(creSigRequ('Testdata'))
