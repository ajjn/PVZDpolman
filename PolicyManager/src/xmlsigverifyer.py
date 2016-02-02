import localconfig
if localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SECLAY:
    from plugins.xmlsigverifyer_moasp import *

__author__ = 'r2h2'


class XmlSigVerifyer():
    def __init__(self):
        if localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SECLAY:
            self.xml_sig_verifier = XmlSigVerifyerMoasp()
        else:
            raise NotImplementedError

    def verify(self, xml_file_name, verify_file_extension=True) -> str:
        if verify_file_extension and xml_file_name[-4:] != '.xml':
            raise InvalidArgumentValueError('XMl filename must have extension .xml')
            # verify xmldsig and extract content

        if localconfig.XMLDSIGLIB == localconfig.XMLDSIGLIB_SECLAY:
            return self.xml_sig_verifier.verify(xml_file_name)
        else:
            raise NotImplementedError
