package at.wien.ma14.pvzd.validatexsd.unittest;


import at.wien.ma14.pvzd.validatexsd.XmlValidator;

import java.net.URL;
import java.net.URLClassLoader;


public class RunValidateXSDcli {

    public void testVerifyGood(String xmldoc) throws Exception {
        ClassLoader cl = ClassLoader.getSystemClassLoader();
        URL[] urls = ((URLClassLoader)cl).getURLs();
        for(URL url: urls){
            System.out.println(url.getFile());
        }

        //String cwd_parent = (new File(new File(".").getAbsolutePath())).getParent();
        XmlValidator validator = new XmlValidator("/Users/admin/devl/java/rhoerbe/PVZD/ValidateXSD/SAML_MD_Schema", true);
        validator.validateSchema(xmldoc);
    }

    public static void main(String[] argv) throws Exception {
        RunValidateXSDcli r = new RunValidateXSDcli();
        r.testVerifyGood(argv[0]);
    }

}