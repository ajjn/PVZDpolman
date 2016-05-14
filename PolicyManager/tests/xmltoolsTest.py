import os.path
from jnius import autoclass
from constants import PROJDIR_ABS
#from xmlsigverifyer import * # XmlSigVerifyer

__author__ = 'r2h2'


class TestXmlTools:
    """
    Used to test java interface and call libraries
    Validates XML schema using Xerces/Java
    Validates XML signature using MOA-ID
    """
    def __init__(self, xsd_schema_dir):
        self.saml_xsd_dir = os.path.join(PROJDIR_ABS, xsd_schema_dir)
        self.pyjnius_xsdvalidator = autoclass('at.wien.ma14.pvzd.validatexsd.XSDValidator')
        self.saml_xsd_validator = self.pyjnius_xsdvalidator(self.saml_xsd_dir, False)

    def validate_xsd(self, filename_abs):
        return self.saml_xsd_validator.validateSchema(filename_abs)

    def validate_schematron(self):
        pass  # TODO: implement


    def verify_xmlsig(self, xml_file_name):
            PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
            verifier = PvzdVerfiySig(
                os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
                os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
                xml_file_name)
            response  = verifier.verify()
            if response.pvzdCode != 'OK':
                raise ValidationError("Signature verification failed, code=" +
                                      response.pvzdCode + "; " + response.pvzdMessage)


if __name__ == '__main__':
    schema_dir_abs = os.path.join(PROJDIR_ABS, 'lib/SAML_MD_Schema')
    testXmlTools = TestXmlTools(schema_dir_abs)
    testXmlTools.validate_xsd('testdata/PAT02_idpExampleCom_sig.xml')
    print('Schema validated')
    testXmlTools.verify_xmlsig('testdata/PMPns05_idp5_signed_untrusted_signer.xml')
    print('Signature validated')
