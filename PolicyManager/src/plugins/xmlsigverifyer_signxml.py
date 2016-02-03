import base64, bz2, datetime, logging, os, re, sys
import signxml
from constants import PROJDIR_ABS
import localconfig
from plugins.xmlsigverifyer_abstract import XmlSigVerifyerAbstract
from userexceptions import ValidationError
from xy509cert import XY509cert
__author__ = 'r2h2'


class XmlSigVerifyerSignxml(XmlSigVerifyerAbstract):
    """ verify xml signatures using python signxml """
    def __init__(self):
        pass

    def verify(self, xml_file_name) -> str:
        """ verify xmldsig and return signerCertificate """
        with open(xml_file_name) as fd:
            xml_str = fd.read()
        with open(localconfig.SIGNCERT) as fd:
            cert = fd.read()
        try:
            verified_et_element = signxml.xmldsig(xml_str.encode('utf-8')).verify(x509_cert=cert)
        except signxml.InvalidDigest:
            logging.info('Invalid digest in ' + xml_file_name)
            raise
        except signxml.InvalidInput:
            logging.info('Invalid input in ' + xml_file_name)
            raise
        return XY509cert.pem_remove_rfc7468_delimiters(cert,
                                                       optional_delimiter=True,
                                                       remove_whitespace=True)
