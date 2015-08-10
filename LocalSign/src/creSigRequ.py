import base64, bz2
import requests
__author__ = 'r2h2'


def creSigRequ(data):

    dataPacked = base64.b64encode(bz2.compress(data))

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
    print r.text

if __name__ == '__main__':
    creSigRequ('Testdata')
