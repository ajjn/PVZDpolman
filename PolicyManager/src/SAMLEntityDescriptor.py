import logging, os, re
import lxml.etree as ET
from jnius import autoclass
from constants import PROJDIR_ABS
from userExceptions import EmptySamlED, InvalidFQDN

__author__ = 'r2h2'


class SAMLEntityDescriptor:
    def __init__(self, filename_abs):
        if not os.path.isfile(filename_abs) or os.path.getsize(filename_abs) == 0:
            raise EmptySamlED(filename_abs + ' empty or missing')
        self.filename_abs = filename_abs
        self.xml_str = open(filename_abs).read()
        self.dom = ET.fromstring(self.xml_str.encode('utf-8'))


    def validateXSD(self):
        xsdValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XSDValidator')
        validator = xsdValidator(os.path.join(PROJDIR_ABS, 'lib/SAML_MD_Schema'), False)
        return validator.validateSchema(self.filename_abs)

    def validateSchematron(self):
        pass  # TODO: implement

    def getNamespacePrefix(self):
        '''
        Due to a limitation in the XML signer used here (SecurityLayer 1.2)
        the XPath expression for the enveloped signature is specified as
        namespace prefix. getNamespacePrefix extracts the prefix to be used
        in the XPath when calling the signature.
        This functions is using a regular expression, YMMV in corner cases.
        '''
        p = re.compile('\sxmlns:(\w+)\s*=\s*"urn:oasis:names:tc:SAML:2.0:metadata"')
        m = p.search(self.xml_str)
        return m.group(1)

    #from urllib.parse import urlparse
    #
    # def validateDomainNames(self, allowedDomains):
    #     ''' list URLs in EntityDescriptor and check vs. allowedDomains.
    #         Checking for valid URLs in values of these attributes:
    #         * EntitiyID
    #         * Location-Attribute
    #     '''
    #     logging.debug('Checking for authorization on entityID')
    #     entityids = _getAttributes('entityID')
    #     for entityid in entityids:
    #         netloc = urlparse(entityid)[1]
    #         logging.debug('   entityID=' + entityid + '; netloc=' + netloc)
    #         if netloc not in allowedDomains:
    #             raise InvalidFQDN('entityid not in allowed domains for authorized signer: ' + entityid)
    #     logging.debug('Checking for authorization on Location attributes')
    #     locs = _getAttributes('Location')
    #     for location in locs:
    #         netloc = urlparse(location)[1]
    #         logging.debug('   Location=' + location + '; netloc=' + netloc)
    #         if location not in allowedDomains:
    #             raise InvalidFQDN('Location not in allowed domains for authorized signer: ' + location)
    #
    # def _getAttributes(self, attrName) -> list:
    #     ''' extract attributes from this EntityDescriptor and return as a list of key-value pairs '''
    #     xslt = '''<?xml version="1.0"?>
    #         <!-- Extract all attributes as key-value pairs -->
    #         <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:dsig="http://www.w3.org/2000/09/xmldsig#" version="1.0">
    #           <xsl:output method="text"/>
    #           <xsl:template match="@*">
    #             <xsl:value-of select="name(.)"/>=<xsl:value-of select="."/>
    #             <xsl:text>&#xa;</xsl:text>
    #           </xsl:template>
    #           <xsl:template match="*">
    #             <xsl:apply-templates select="@*"/>
    #             <xsl:apply-templates select="*"/>
    #           </xsl:template>
    #         </xsl:stylesheet>'''
    #     xslt = ET.fromstring(xslt.encode('utf-8'))
    #     transform = ET.XSLT(xslt)
    #     attributes = []
    #     for line in str(transform(dom)).splitlines():
    #         (attr_name, attr_val) = line.split('=')
    #         attr_name = re.sub('^\w+:', '', attr_name)
    #         if attr_name == attrName:
    #             attributes.append([attr_name, attr_val])
    #     return attributes


