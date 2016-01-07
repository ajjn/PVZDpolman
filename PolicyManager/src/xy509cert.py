import re
from datetime import datetime
from OpenSSL import crypto
__author__ = 'r2h2'


class XY509cert:
    ''' Wrapper for OpenSSL.crypto.x509 to add a few methods. (yes, could have
        been done with a subclass as well)
    '''
    def __init__(self, cert_str, inform='PEM'):
        if inform == 'PEM':
            hasStartLine = False
            for l in cert_str.splitlines(True):
                if l == '-----BEGIN CERTIFICATE-----\n':
                    hasStartLine = True
                    break
            if not hasStartLine:
                c =  '-----BEGIN CERTIFICATE-----\n' + cert_str + '\n-----END CERTIFICATE-----\n'
                c = re.sub('\n\s*\n', '\n', c) # openssl dislikes blank lines before the end line
            else:
                c = cert_str
            self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, c)
        elif inform == 'DER':
            self.cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_str)
        self.cert_str = cert_str

    def getPEM_str(self) -> str:
        ''' from the multi-line string in self.cert_str extract text between -----BEGIN and END----- markers'''
        begin = False
        end = False
        pem_str = ''
        for l in self.cert_str.splitlines(True):
            if l == '-----BEGIN CERTIFICATE-----\n':
                begin = True
                continue
            if begin:
                if l.startswith('-----END CERTIFICATE-----'):
                    end = True
                    break
                pem_str += l
        if not begin:
            raise ValidationFailure("PEM file must have '-----BEGIN CERTIFICATE-----' header conforming to RFC 7468")
        if not end:
            raise ValidationFailure("PEM file must have '-----END CERTIFICATE-----' header conforming to RFC 7468")
        return pem_str

    def getSubjectCN(self) -> str:
        subject_dn = self.cert.get_subject()
        for (k, v) in subject_dn.get_components():
            if k.decode('utf-8') == 'CN':
                return v.decode('utf-8')

    def getSubject_str(self) -> str:
        subject_dn = self.cert.get_subject()
        subject_str = str(subject_dn).replace("<X509Name object '", '')[:-2]
        return subject_str

    def getIssuer_str(self) -> str:
        issuer_dn = self.cert.get_issuer()
        issuer_str = str(issuer_dn).replace("<X509Name object '", '')[:-2]
        return issuer_str

    def isNotExpired(self) -> bool:
        notValidAfter_str = self.cert.get_notAfter().decode('ascii')
        notValidAfter_date = datetime.strptime(notValidAfter_str, '%Y%m%d%H%M%SZ')
        return notValidAfter_date > datetime.now()