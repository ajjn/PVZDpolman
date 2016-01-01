import os, re
from jnius import autoclass
from userExceptions import EmptySamlED

__author__ = 'r2h2'


class SAMLEntityDescriptor:
    def __init__(self, filename_abs, projdir_abs):
        if not os.path.isfile(filename_abs) or os.path.getsize(filename_abs) == 0:
            raise EmptySamlED(filename_abs + ' empty or missing')
        self.filename_abs = filename_abs
        self.projdir_abs = projdir_abs

    def validateXSD(self):
        xsdValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XSDValidator')
        validator = xsdValidator(os.path.join(self.projdir_abs, 'lib/SAML_MD_Schema'), False)
        return validator.validateSchema(self.filename_abs)

    def getNamespacePrefix(self):
        '''
        Due to a limitation in the XML signer used here (SecurityLayer 1.2)
        the XPath expression for the enveloped signature is specified as
        namespace prefix. getNamespacePrefix extracts the prefix to be used
        in the XPath when calling the signature.
        This functions is using a regular expression, YMMV in corner cases.
        '''
        xml_str = open(self.filename_abs).read()
        p = re.compile('\sxmlns:(\w+)\s*=\s*"urn:oasis:names:tc:SAML:2.0:metadata"')
        m = p.search(xml_str)
        return m.group(1)

