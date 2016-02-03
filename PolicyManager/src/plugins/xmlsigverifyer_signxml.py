import base64, bz2, datetime, os, re, sys
from signxml import *
from constants import PROJDIR_ABS
import localconfig
from plugins.xmlsigverifyer_abstract import XmlSigVerifyerAbstract
from userexceptions import ValidationError
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
        verified_et_element = xmldsig(xml_str.encode('utf-8')).verify(x509_cert=cert)
        return cert
