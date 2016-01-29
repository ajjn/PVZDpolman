import os.path
from jnius import autoclass
from constants import PROJDIR_ABS

__author__ = 'r2h2'


class XmlSchemaValidator:
    """
    Validates XML schema using Xerces/Java
    """
    def __init__(self, xsd_schema_dir):
        self.saml_xsd_dir = os.path.join(PROJDIR_ABS, xsd_schema_dir)
        self.pyjnius_xsdvalidator = autoclass('at.wien.ma14.pvzd.validatexsd.XSDValidator')
        self.saml_xsd_validator = self.pyjnius_xsdvalidator(self.saml_xsd_dir, False)


    def validate_xsd(self, filename_abs):
        return self.saml_xsd_validator.validateSchema(filename_abs)

    def validate_schematron(self):
        pass  # TODO: implement

