import re
from datetime import datetime
from OpenSSL import crypto as c
__author__ = 'r2h2'

class X509cert:
    def __init__(self, cert_str):
        assert cert_str.startswith('-----BEGIN CERTIFICATE-----'), "PEM file must have '-----BEGIN CERTIFICATE-----' header"
        assert re.findall(r'-----END CERTIFICATE-----\n*$', cert_str), "PEM file must have '-----END CERTIFICATE-----' trailer"
        self.cert = c.load_certificate(c.FILETYPE_PEM, cert_str)
        self.cert_str = cert_str

    def getPEM_str(self):
        pem_no_header = re.sub(r'-----BEGIN CERTIFICATE-----\n', '', self.cert_str)
        pem_str = re.sub(r'\n-----END CERTIFICATE-----\n*$', '\n', pem_no_header)
        return pem_str

    def getSubjectCN(self):
        subject_dn = self.cert.get_subject()
        for (k, v) in subject_dn.get_components():
            if k.decode('utf-8') == 'CN':
                return v.decode('utf-8')

    def getIssuer_str(self):
        issuer_dn = self.cert.get_issuer()
        issuer_str = str(issuer_dn).replace("<X509Name object '", '')[:-2]
        return issuer_str

    def isNotExpired(self):
        notValidAfter_str = self.cert.get_notAfter()
        notValidAfter_date = datetime.strptime(notValidAfter_str, '%Y%m%d%H%M%SZ')
        return notValidAfter_date > datetime.now()
