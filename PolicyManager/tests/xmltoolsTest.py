import os.path
from jnius import autoclass
from constants import PROJDIR_ABS

__author__ = 'r2h2'


class TestXmlTools:
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

if __name__ == '__main__':
    schema_dir_abs = os.path.join(PROJDIR_ABS, 'lib/SAML_MD_Schema')
    saml_schema_validator = TestXmlTools(schema_dir_abs)
    saml_schema_validator.validate_xsd('testdata/PAT02_idpExampleCom_sig.xml')
    print('Schema validated')
