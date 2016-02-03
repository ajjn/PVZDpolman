import base64, bz2, datetime, os, re, sys
from signxml import *
from constants import PROJDIR_ABS
from userexceptions import ValidationError
import XmlSigVerifyerSignxmlAbstract
__author__ = 'r2h2'


class XmlSigVerifyerSignxml(XmlSigVerifyerAbstract):
    """ verify xml signatures using python signxml """
    def __init__(self):
        pass

    def verify(self, xml_file_name) -> str:
        """ verify xmldsig and return signerCertificate """
        xml_str = open(xml_file_name).read()
        cert = open(localconfig.SIGNCERT).read()
        verified_et_element = xmldsig(xml_str).verify(x509_cert=cert)
        return response.signerCertificateEncoded
