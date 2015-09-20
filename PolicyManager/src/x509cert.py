from datetime import datetime
from OpenSSL import crypto as c
__author__ = 'r2h2'

class X509cert:
    def __init__(self, cert_str):
        self.cert = c.load_certificate(c.FILETYPE_PEM, cert_str)

    def getSubjectCN(self):
        subject_dn = self.cert.get_subject()
        for (k, v) in subject_dn:
            if k == 'CN':
                return v

    def getIssuer_str(self):
        issuer_dn = self.cert.get_issuer()
        issuer_str = str(issuer_dn).replace("<X509Name object '", '')[:-2]
        return issuer_str

    def isNotExpired(self):
        notValidAfter_str = self.cert.get_notAfter()
        notValidAfter_date = datetime.strptime(notValidAfter_str, '%Y%m%d%H%M%SZ')
        return notValidAfter_date > datetime.now()
