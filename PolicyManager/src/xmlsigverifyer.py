import localconfig
if localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SECLAY:
    from plugins.xmlsigverifyer_moasp import *
elif localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SIGNXML:
    from plugins.xmlsigverifyer_signxml import *

__author__ = 'r2h2'


class XmlSigVerifyer():
    def __init__(self):
        if localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SECLAY:
            self.xml_sig_verifier = XmlSigVerifyerMoasp()
        elif localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SIGNXML:
            self.xml_sig_verifier = XmlSigVerifyerSignXml()
        else:
            raise NotImplementedError

    def verify(self, xml_file_name, verify_file_extension=True) -> str:
        """ verify xmldsig and return signerCertificate """
        if verify_file_extension and xml_file_name[-4:] != '.xml':
            raise InvalidArgumentValueError('XMl filename must have extension .xml')


        return self.xml_sig_verifier.verify(xml_file_name)
