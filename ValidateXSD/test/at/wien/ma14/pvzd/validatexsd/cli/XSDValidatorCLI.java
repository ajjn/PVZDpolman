package at.wien.ma14.pvzd.validatexsd.cli;


import at.wien.ma14.pvzd.validatexsd.XSDValidator;
import java.net.URL;
import java.net.URLClassLoader;


public class XSDValidatorCLI {

    public void testVerifyGood(String xmldoc, String samlxsdDir) throws Exception {
        ClassLoader cl = ClassLoader.getSystemClassLoader();
        URL[] urls = ((URLClassLoader)cl).getURLs();
        for(URL url: urls){
            System.out.println(url.getFile());
        }

        //String cwd_parent = (new File(new File(".").getAbsolutePath())).getPare0nt();
        XSDValidator validator = new XSDValidator(samlxsdDir, true);
        validator.validateSchema(xmldoc);
    }

    public static void main(String[] argv) throws Exception {
        System.out.println("XSDValidatorCLI ..");
        XSDValidatorCLI r = new XSDValidatorCLI();
        if (argv.length == 1) {
            r.testVerifyGood(argv[0], "/Users/admin/devl/java/rhoerbe/PVZD/ValidateXSD/SAML_MD_Schema");
        } else if (argv.length == 2) {
            r.testVerifyGood(argv[0], argv[1]);
        } else {
            System.out.println("XSDValidatorCLI <file-to-be-validated> [schema-dir]");
        }
    }

}