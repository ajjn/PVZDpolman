package at.wien.ma14.pvzd.validatexsd.unittest;


import at.wien.ma14.pvzd.validatexsd.XmlValidator;
import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;


public class RunVerifyXSD {
    final File log4jprop = new File("VerifySigAPI/conf/log4j.properties");
    final File moaspprop = new File("/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml");

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
        RunVerifyXSD r = new RunVerifyXSD();
        r.testVerifyGood();
    }

}