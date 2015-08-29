package at.wien.ma14.pvzd.verifysigapi.validateXSD;

import org.junit.Test;

public class XmlValidatorTest {

    @Test
    public void testValidateOK() throws Exception {
        final String samlmdFileOK = "ValidateXSD/testdata/idp5_valid.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema");
        validator.validateSchema(samlmdFileOK);
    }

    @Test(expected = org.xml.sax.SAXParseException.class)
    public void testValidateNotSchemaConforming() throws Exception {
        final String samlmdFileOK = "ValidateXSD/testdata/idp5_not_schema_valid.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema");
        validator.validateSchema(samlmdFileOK);
    }

    @Test(expected = org.xml.sax.SAXParseException.class)
    public void testValidateNoWellformedXML() throws Exception {
        final String samlmdFileOK = "ValidateXSD/testdata/idp5_invalid_xml.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema");
        validator.validateSchema(samlmdFileOK);
    }

}