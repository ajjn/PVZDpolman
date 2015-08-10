/**
 * Extract all signing certificates from SAML metadata (i.e. in IDPSSODescriptor and SPSSPDescriptor elements)
 *
 * @author r2h2, 2015-02-28
 */
//package at.gv.portalverbund.tools.metadata

import javax.xml.parsers.*;
import javax.xml.xpath.*;
import org.w3c.dom.*;

class ExtractCertsXPath {

    static main(args) {
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document dDoc = builder.parse("/Users/admin/admin/netcup4/srv/httpd/mdTestPortalverbundGvAt/html/testfed-metadata.xml");

        def xPath = XPathFactory.newInstance().newXPath();
        def nodelist = xPath.evaluate("/EntitiesDescriptor/EntityDescriptor/@entityID", dDoc, XPathConstants.NODESET);
        def numEDs = nodelist.getLength();

        nodelist.each{
            def entityid = it.getFirstChild().getNodeValue();
            def certpath = '/EntitiesDescriptor/EntityDescriptor[@entityID=' + "'" + entityid + "']" +
                    '/IDPSSODescriptor/KeyDescriptor/KeyInfo/X509Data'
            println 'certpath: ' + certpath
            def nodelist2 = xPath.evaluate(certpath, dDoc, XPathConstants.NODESET);
            println ".. printing certificates for entity " + entityid;
            nodelist2.each{
                def cert = it.getFirstChild().getNodeValue();
                println cert;
            }
        }
        println("query returned " + numEDs + " nodes.");
    }

}
