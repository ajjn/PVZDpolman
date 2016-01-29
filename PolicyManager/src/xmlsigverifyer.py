import base64, bz2, datetime, os, re, sys
from jnius import autoclass
from constants import PROJDIR_ABS
from userexceptions import InvalidArgumentValueError, ValidationError
from xmlsigverifyer import XmlSigVerifyer
__author__ = 'r2h2'


class XmlSigVerifyer():
    def __init__(self, verifyer_lib='MOAID'):
        assert verifyer_lib in ('MOAID',), 'verifier lib "' + '" not supported'
        self.verifyer_lib = verifyer_lib

    def verify(self, xml_file_name, verify_file_extension=True) -> str:
        if verify_file_extension and xml_file_name[-4:] != '.xml':
            raise InvalidArgumentValueError('XMl filename must have extension .xml')
            # verify xmldsig and extract content
        if self.verifyer_lib == 'MOAID':
            PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
            verifier = PvzdVerfiySig(
                os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
                os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
                xml_file_name)
            response  = verifier.verify()
            if response.pvzdCode != 'OK':
                raise ValidationError("Signature verification failed, code=" +
                                      response.pvzdCode + "; " + response.pvzdMessage)
            return response.signerCertificateEncoded
