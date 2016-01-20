import base64, bz2, sys
import logging
import requests
import re
import socket
from constants import DATA_HEADER_B64BZIP
from userExceptions import *

__author__ = 'r2h2'

def failIfSecurityLayerUnavailable():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('127.0.0.1', 3495)
    if sock.connect_ex(addr) != 0:
        sys.tracebacklimit = 0
        raise SecurityLayerUnavailable(SecurityLayerUnavailable.__doc__)
    sock.close()

def getSecLayRequestTemplate(sigType, sigPosition=None) -> str:
    ''' return an XML template to be merged with the data to be signed
        sigPosition is the XPath for the element under which an enveoped signature shall
        be positioned, e.g. <md:/EntitiyDescriptor>
    '''
    if sigType == 'envelopingB64BZIP':
        return '''\
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
</sl:CreateXMLSignatureRequest> '''
    if sigType == 'enveloped':
        return '''\
<?xml version="1.0" encoding="UTF-8"?>
<sl:CreateXMLSignatureRequest
  xmlns:sl="http://www.buergerkarte.at/namespaces/securitylayer/1.2#">
  <sl:KeyboxIdentifier>SecureSignatureKeypair</sl:KeyboxIdentifier>
  <sl:DataObjectInfo Structure="detached">
    <sl:DataObject Reference=""></sl:DataObject>
    <sl:TransformsInfo>
	<dsig:Transforms xmlns:dsig="http://www.w3.org/2000/09/xmldsig#">
        <dsig:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
      </dsig:Transforms>
      <sl:FinalDataMetaInfo>
        <sl:MimeType>application/xml</sl:MimeType>
      </sl:FinalDataMetaInfo>
    </sl:TransformsInfo>
  </sl:DataObjectInfo>
  <sl:SignatureInfo>
    <sl:SignatureEnvironment>
      <sl:XMLContent>
%s
      </sl:XMLContent>
    </sl:SignatureEnvironment>
    <sl:SignatureLocation xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" Index="0">%s</sl:SignatureLocation>
  </sl:SignatureInfo>
</sl:CreateXMLSignatureRequest> ''' % ('%s', sigPosition)

def creSignedXML(data, sigType='envelopingB64BZIP', sigPosition=None, verbose=False):
    ''' Create XAdES signature using AT Bürgerkarte/Security Layer
        There are two signature types:
            1. envelopingB64BZIP: compress, b64-encode and sign the data (enveloping)
            2. enveloped: sign whole element specified py the XPath location
        Caveat: the XPAth for the position of the enveloping signature must use the
            QName prefix, not the namespace URI
            (e.g. md: instead of urn:oasis:names:tc:SAML:2.0:metadata:)
    '''

    if sigType not in ('envelopingB64BZIP', 'enveloped'):
        raise ValidationFailure("Signature type must be one of 'envelopingB64BZIP', 'enveloped' but is " + sigType)
    failIfSecurityLayerUnavailable()
    if sigType == 'envelopingB64BZIP':
        dataObject = DATA_HEADER_B64BZIP + base64.b64encode(bz2.compress(data.encode('utf-8'))).decode('ascii')
    else:
        dataObject = re.sub('<\?xml.*>', '', data)  #remove xml-header - provided by SecLay request wrapper
    logging.debug('data to be signed:\n%s\n\n' % dataObject)
    sigRequ = getSecLayRequestTemplate(sigType, sigPosition) % dataObject
    logging.debug('SecLay request:\n%s\n' % sigRequ)
    try:
        r = requests.post('http://localhost:3495/http-security-layer-request',
                          data={'XMLRequest': sigRequ})
    except requests.exceptions.ConnectionError as e:
        raise ValidationFailure("Cannot connect to security layer (MOCCA) to create a signature " + e.strerror)
    if r.status_code != 200:
        raise ValidationFailure("Security layer failed with HTTP %s, message: \n\n%s" % (r.status_code, r.text))
    if r.text.find('sl:ErrorResponse') >= 0:
        raise ValidationFailure("Security Layer responed with error message.\n" + r.text)

    # Strip xml root element (CreateXMLSignatureResponse), making disg:Signature the new root:
    # (keeping namespace prefixes - otherwise the signature would break. Therefore not using etree.)
    logging.debug('security layer create signature response:\n%s\n' % r.text)
    r1 = re.sub(r'<sl:CreateXMLSignatureResponse [^>]*>', '', r.text)
    r2 = re.sub(r'</sl:CreateXMLSignatureResponse>', '', r1)
    return r2


if __name__ == '__main__':
    ''' main for simplified command-line tests of XML documents with a dummy md:EntityDescriptor as root element'''
    print("args=" + sys.argv[1] + "\n")
    if sys.argv[1] == 'Enveloping':
        print("Enveloping signature\n")
        print(creSignedXML('Test string', verbose=True))
    elif sys.argv[1] == 'Enveloped':
        print("Enveloped signature\n")
        ed = '''\
<md:EntityDescriptor entityID="https://gondor.magwien.gv.at/idp"
    xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
            <ds:X509Certificate>MIIFxjCCBK6gAwIBAgICAlswDQYJKoZIhvcNAQELBQAwgZgxCzAJBgNVBAYTAkFUMQ0wCwYDVQQIEwRXaWVuMScwJQYDVQQKEx5CdW5kZXNtaW5pc3Rlcml1bSBmdWVyIElubmVyZXMxDjAMBgNVBAsTBUlULU1TMRkwFwYDVQQDExBQb3J0YWx2ZXJidW5kLUNBMSYwJAYJKoZIhvcNAQkBFhdibWktaXYtMi1lLWNhQGJtaS5ndi5hdDAeFw0xNTA3MTUwNzU2MTNaFw0xNzA4MDMwNzU2MTNaMIGEMQswCQYDVQQGEwJBVDEhMB8GA1UEChMYTWFnaXN0cmF0IGRlciBTdGFkdCBXaWVuMQ4wDAYDVQQLEwVNQSAxNDEdMBsGA1UEAxMUZ29uZG9yLm1hZ3dpZW4uZ3YuYXQxIzAhBgkqhkiG9w0BCQEWFHBvc3RAbWExNC53aWVuLmd2LmF0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2wvSx495pwJlN6ILaz+/0TQKARv7U0vJLggmQBheYhka5nEt6Oq9d2Zd6/QlTLSVcNp0GCZ3f1kMj842MatnGqAPdmtnSEQTLsOb6hKOC1ZE1g2yKJYxM7iyjsb+ZVCnfDZegn+P5n06Gzzh8UlQvD5h/lGVE//PZAu35oY2IpSAkvFEke8sT9ZdqFGWdcLFnzpt8JHbvfHLgWC63N/7UbVuLBQ/no0ynJBlUB+RGm1G+HkZl1SxNg9ul4Sakil/IiXadA+Cc9XEaV/W0dV2HEzkS8mtSY75bjMs0jiepwxAzKwi09Sfo8xrs8VyG6hkwF63+PyqtL5V3MS2LOR/awIDAQABo4ICKjCCAiYwCQYDVR0TBAIwADALBgNVHQ8EBAMCBeAwLAYJYIZIAYb4QgENBB8WHU9wZW5TU0wgR2VuZXJhdGVkIENlcnRpZmljYXRlMB0GA1UdDgQWBBQwexiDS7rYLmA4t03y7Gj1xoV6MTCB0QYDVR0jBIHJMIHGgBSmHvReGkO0iN6iyL1oZQPFMG9m06GBqqSBpzCBpDELMAkGA1UEBhMCQVQxDTALBgNVBAgTBFdpZW4xDTALBgNVBAcTBFdpZW4xJzAlBgNVBAoTHkJ1bmRlc21pbmlzdGVyaXVtIGZ1ZXIgSW5uZXJlczEOMAwGA1UECxMFSVQtTVMxFjAUBgNVBAMTDVBvcnRhbFJvb3QtQ0ExJjAkBgkqhkiG9w0BCQEWF2JtaS1pdi0yLWUtY2FAYm1pLmd2LmF0ggEBMB8GA1UdEQQYMBaBFHBvc3RAbWExNC53aWVuLmd2LmF0MCIGA1UdEgQbMBmBF2JtaS1pdi0yLWUtY2FAYm1pLmd2LmF0MEUGA1UdHwQ+MDwwOqA4oDaGNGh0dHA6Ly9wb3J0YWwuYm1pLmd2LmF0L3JlZi9wa2kvcG9ydGFsQ0EvUG9ydGFsVi5jcmwwTwYIKwYBBQUHAQEEQzBBMD8GCCsGAQUFBzAChjNodHRwOi8vcG9ydGFsLmJtaS5ndi5hdC9yZWYvcGtpL3BvcnRhbENBL2luZGV4Lmh0bWwwDgYHKigACgEBAQQDAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQACkWwa0E3XcQRO0Z77wCqQpWyalFv6TH9OD9GQkXsg5P24Uqrm6Cpfq0wd612EfC5y4hqTz2nOqNHo6lcvoMOQimjimZTp4tLcMgqTt5NxniEKsRhH/4OKMrtaK7/erwn/8PyK7zT+NwTXo2UhTLW1eO8E2irItZ1jyN8fuj1J3OfoEJ3H+NSxWuSxr7pbNy7HvnPtGqPOlpgw4nhRQM5OP0CJxSbwO1hpBM5vd+yEauXZrCxv7AZCL7SqkRvIV2D4wnr9ddAsH2eGwXfKVgXKD46Z+S8L9CL/EUQdlEULqI5PlQ9qJWKp5P5UMvBd0SM0Tvd6WnJYA11vS6LM0bHG</ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://gondor.magwien.gv.at/R-Profil-dummy"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>'''
        ed = '''\
<?xml version="1.0" encoding="UTF-8"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:alg="urn:oasis:names:tc:SAML:metadata:algsupport" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:mdui="urn:oasis:names:tc:SAML:metadata:ui" entityID="https://idp.example.com/idp.xml">
    <md:IDPSSODescriptor WantAuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
         <md:Extensions>
            <alg:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
            <alg:SigningMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256" MaxKeySize="511" MinKeySize="256"/>
            <alg:SigningMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" MaxKeySize="4096" MinKeySize="2048"/>
            <!-- blacklisted: http://www.w3.org/2000/09/xmldsig#rsa-sha1 -->
            <mdui:UIInfo>
                <mdui:DisplayName xml:lang="en">Test Driver IdP </mdui:DisplayName>
                <mdui:Description xml:lang="en">Saml2Test Test Driver IdP</mdui:Description>
            </mdui:UIInfo>
            <mdui:DiscoHints>
                <mdui:DomainHint>https://github.com/rohe/fedlab/</mdui:DomainHint>
                <mdui:IPHint>81.217.70.0/8</mdui:IPHint>
                <mdui:GeolocationHint>geo:92.3308,17.0516</mdui:GeolocationHint>
            </mdui:DiscoHints>
        </md:Extensions>
        <md:KeyDescriptor use="signing">
            <ds:KeyInfo>
                <ds:X509Data>
                    <ds:X509Certificate>MIIC8jCCAlugAwIBAgIJAJHg2V5J31I8MA0GCSqGSIb3DQEBBQUAMFoxCzAJBgNVBAYTAlNFMQ0wCwYDVQQHEwRVbWVhMRgwFgYDVQQKEw9VbWVhIFVuaXZlcnNpdHkxEDAOBgNVBAsTB0lUIFVuaXQxEDAOBgNVBAMTB1Rlc3QgU1AwHhcNMDkxMDI2MTMzMTE1WhcNMTAxMDI2MTMzMTE1WjBaMQswCQYDVQQGEwJTRTENMAsGA1UEBxMEVW1lYTEYMBYGA1UEChMPVW1lYSBVbml2ZXJzaXR5MRAwDgYDVQQLEwdJVCBVbml0MRAwDgYDVQQDEwdUZXN0IFNQMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDkJWP7bwOxtH+E15VTaulNzVQ/0cSbM5G7abqeqSNSs0l0veHr6/ROgW96ZeQ57fzVy2MCFiQRw2fzBs0n7leEmDJyVVtBTavYlhAVXDNa3stgvh43qCfLx+clUlOvtnsoMiiRmo7qf0BoPKTj7c0uLKpDpEbAHQT4OF1HRYVxMwIDAQABo4G/MIG8MB0GA1UdDgQWBBQ7RgbMJFDGRBu9o3tDQDuSoBy7JjCBjAYDVR0jBIGEMIGBgBQ7RgbMJFDGRBu9o3tDQDuSoBy7JqFepFwwWjELMAkGA1UEBhMCU0UxDTALBgNVBAcTBFVtZWExGDAWBgNVBAoTD1VtZWEgVW5pdmVyc2l0eTEQMA4GA1UECxMHSVQgVW5pdDEQMA4GA1UEAxMHVGVzdCBTUIIJAJHg2V5J31I8MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAMuRwwXRnsiyWzmRikpwinnhTmbooKm5TINPE7A7gSQ710RxioQePPhZOzkM27NnHTrCe2rBVg0EGz7QTd1JIwLPvgoj4VTi/fSha/tXrYUaqc9AqU1kWI4WN                        +vffBGQ09mo+6CffuFTZYeOhzP/2stAPwCTU4kxEoiy0KpZMANI=
                    </ds:X509Certificate>
                </ds:X509Data>
            </ds:KeyInfo>
        </md:KeyDescriptor>
        <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://idp.example.com/slo/post"/>
        <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://idp.example.com/slo/redirect"/>
        <md:ManageNameIDService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://idp.example.com/mni/post"/>
        <md:ManageNameIDService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://idp.example.com/mni/redirect"/>
        <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
        <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:persistent</md:NameIDFormat>
        <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://idp.example.com/sso/redirect"/>
        <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://idp.example.com/sso/post"/>
        <md:AssertionIDRequestService Binding="urn:oasis:names:tc:SAML:2.0:bindings:URI" Location="https://idp.example.com/airs"/>
    </md:IDPSSODescriptor>
    <md:Organization>
        <md:OrganizationName xml:lang="en">Saml2Test Harness</md:OrganizationName>
        <md:OrganizationDisplayName xml:lang="en">Saml2Test Harness</md:OrganizationDisplayName>
        <md:OrganizationURL xml:lang="en">https://github.com/rohe/saml2test/</md:OrganizationURL>
    </md:Organization>
    <md:ContactPerson contactType="technical">
        <md:GivenName>Testiani</md:GivenName>
        <md:SurName>Testosteroni</md:SurName>
        <md:EmailAddress>testiani@example.com</md:EmailAddress>
    </md:ContactPerson>
</md:EntityDescriptor>'''

        print(creSignedXML(ed, 'enveloped', sigPosition='/md:EntityDescriptor', verbose=True))
    else: print('invalid argument')