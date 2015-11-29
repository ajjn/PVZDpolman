package at.wien.ma14.pvzd.validatexsd.unittest;


import at.wien.ma14.pvzd.validatexsd.XmlValidator;
import java.net.URL;
import java.net.URLClassLoader;


public class RunValidateXSD {

    public void testVerifyGood() throws Exception {
        ClassLoader cl = ClassLoader.getSystemClassLoader();
        URL[] urls = ((URLClassLoader)cl).getURLs();
        for(URL url: urls){
            System.out.println(url.getFile());
        }

        final String samlmdFileOK = "ValidateXSD/testdata/idp5_valid.xml";
        XmlValidator validator = new XmlValidator("ValidateXSD/SAML_MD_Schema", true);
        validator.validateSchema(samlmdFileOK);    }

    public static void main(String[] argv) throws Exception {
        RunValidateXSD r = new RunValidateXSD();
        r.testVerifyGood();
    }

}