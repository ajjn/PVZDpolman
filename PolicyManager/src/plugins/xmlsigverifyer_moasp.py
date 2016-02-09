import base64, bz2, datetime, os, re, sys
from jnius import autoclass
from constants import PROJDIR_ABS
from plugins.xmlsigverifyer_abstract import XmlSigVerifyerAbstract
from userexceptions import *

__author__ = 'r2h2'


class XmlSigVerifyerMoasp(XmlSigVerifyerAbstract):
    """ Python wrapper for the PvzdVerifySig Java class """
    def __init__(self):
        self.pywrapper = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')

    def verify(self, xml_file_name) -> str:
        """ verify xmldsig and return signerCertificate """
        pvzdverifysig = self.pywrapper(
            os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
            os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
            xml_file_name)
        response  = pvzdverifysig.verify()
        if response.pvzdCode != 'OK':
            raise ValidationError("Signature verification failed, code=" +
                                  response.pvzdCode + "; " + response.pvzdMessage)
        return response.signerCertificateEncoded
