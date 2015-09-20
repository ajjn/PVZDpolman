package at.wien.ma14.pvzd.validatexsd.unittest;

import at.wien.ma14.pvzd.validatexsd.XmlValidator;
import org.junit.Test;
import static org.junit.Assert.*;

public class XmlValidatorUT {
//    public void XMLValidatorTest() {}

    @Test
    public void test01_ValidateOK() throws Exception {
        final String samlmdFileOK = "ValidateXSD/testdata/idp5_valid.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema", true);
        String m = validator.validateSchema(samlmdFileOK);
        assertNull("expected null message but received: " + m, m);
    }

    @Test
    public void test02_ValidateNotSchemaConforming() throws Exception {
        final String samlmdFileNOK = "ValidateXSD/testdata/idp5_not_schema_valid.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema", true);
        String m = validator.validateSchema(samlmdFileNOK);
        assertNotNull("expected message but received null", m);
    }

    @Test
    public void tes03_tValidateNoWellformedXML() throws Exception {
        final String samlmdFileNOK = "ValidateXSD/testdata/idp5_invalid_xml.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema", true);
        String m = validator.validateSchema(samlmdFileNOK);
        assertNotNull("expected message but received null", m);
    }

}