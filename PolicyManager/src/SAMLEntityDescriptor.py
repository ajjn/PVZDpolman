import logging, os, re
import lxml.etree as ET
from constants import PROJDIR_ABS
from xmlschemavalidator import XmlSchemaValidator
from userexceptions import EmptySamlEDError

__author__ = 'r2h2'


class SAMLEntityDescriptor:
    def __init__(self, filename_abs):
        if not os.path.isfile(filename_abs) or os.path.getsize(filename_abs) == 0:
            raise EmptySamlEDError(filename_abs + ' empty or missing')
        self.filename_abs = filename_abs
        with open(filename_abs) as f:
            self.xml_str = f.read()
        self.dom = ET.fromstring(self.xml_str.encode('utf-8'))


    def validate_xsd(self):
        schema_dir_abs = os.path.join(PROJDIR_ABS, 'lib/SAML_MD_Schema')
        saml_schema_validator = XmlSchemaValidator(schema_dir_abs, False)
        return saml_schema_validator.validate_xsd(self.filename_abs)

    def validate_schematron(self):
        pass  # TODO: implement

    def get_namespace_prefix(self):
        '''
        Due to a limitation in the XML signer used here (SecurityLayer 1.2)
        the XPath expression for the enveloped signature is specified as
        namespace prefix. getNamespacePrefix extracts the prefix to be used
        in the XPath when calling the signature.
        This functions is using a regular expression, YMMV in corner cases.
        '''
        p = re.compile('\sxmlns:(\w+)\s*=\s*"urn:oasis:names:tc:SAML:2.0:metadata"')
        m = p.search(self.xml_str)
        return m.group(1)

