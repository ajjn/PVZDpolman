import re
from datetime import datetime
from OpenSSL import crypto as c
__author__ = 'r2h2'

class X509cert:
    def __init__(self, cert_str):
        self.cert = c.load_certificate(c.FILETYPE_PEM, cert_str)
        self.cert_str = cert_str

    def getPEM_str(self):
        ''' from the multi-line string in self.cert_str extract text between -----BEGIN and END----- markers'''
        begin = False
        end = False
        pem_str = ''
        for l in self.cert_str.splitlines(True):
            if l == '-----BEGIN CERTIFICATE-----\n':
                begin = True
            if begin:
                if l.startswith('-----END CERTIFICATE-----'):
                    end = True
                    break
                pem_str += l
        assert begin, "PEM file must have '-----BEGIN CERTIFICATE-----' header conforming to RFC 7468"
        assert end, "PEM file must have '-----END CERTIFICATE-----' header conforming to RFC 7468"
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
