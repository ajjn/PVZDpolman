package at.wien.ma14.pvzd;

import org.junit.Test;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.Assert.*;

/**
 * Created by r2h2 on 10.08.15.
 */
public class verfiySigTest {
    @Test
    public void testVerifyGood() throws Exception {
        PvzdVerfiySig verifier  = new PvzdVerfiySig(
                "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
                "conf/log4j.properties",
                "testdata/idp5_valid.xml_sig.xml");
        PvzdVerifySigResponse response  = verifier.verify();
        assertEquals("Expected OK for messageID", response.pvzdCode, "OK");
        String cert_b64 = new String(Files.readAllBytes(Paths.get("testdata/r2h2_ecard_qcert.b64")));
        assertEquals("Certificate mismatch", response.signerCertificateEncoded, cert_b64);
    }

    @Test
    public void testVerifySignatureValueBroken() throws Exception {
        PvzdVerfiySig verifier  = new PvzdVerfiySig(
                "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
                "conf/log4j.properties",
                "testdata/idp5_invalid.xml_sig.xml");
        PvzdVerifySigResponse response  = verifier.verify();
        assertEquals("Expected NOK for messageID", response.pvzdCode, "NOK");
    }
}