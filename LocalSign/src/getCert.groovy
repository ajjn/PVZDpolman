def xml = new File('/Users/admin/devl/pycharm/rhoerbe/saml_schematron/testdata/idp5_valid.xml').text

def envelope = new XmlSlurper().parseText(xml)
envelope.declareNamespace(
        md:'urnoasisnamestcSAML20metadata')
//'md': 'urn:oasis:names:tc:SAML:2.0:metadata')
/*,        mdattr = "urn:oasis:names:tc:SAML:metadata:attribute",
        xrd = "http://docs.oasis-open.org/ns/xri/xrd-1.0",
        mdrpi = "urn:oasis:names:tc:SAML:metadata:rpi",
        mdui = "urn:oasis:names:tc:SAML:metadata:ui",
        alg = "urn:oasis:names:tc:SAML:metadata:algsupport",
        disco = "urn:oasis:names:tc:SAML:profiles:SSO:idp-discovery-protocol",
        ds = "http://www.w3.org/2000/09/xmldsig#"
)*/

println 'xpath:'
println envelope.'md:EntitiesDescriptor'.'md:EntityDescriptor'.'@entityID'

/* assert 'Some Service^V100' == envelope.'s:Body'.
't:About_ServiceResponse'.
't:About_ServiceResult'.
'a:businessServiceVersionStructureField'.
'a:BusinessServiceVersionStructureType'.
'a:businessServiceVersionNameField'.text()
*/