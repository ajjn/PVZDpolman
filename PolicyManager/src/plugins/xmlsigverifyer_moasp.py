import base64, bz2, datetime, os, re, sys
from jnius import autoclass
import lxml.etree as ET
from constants import PROJDIR_ABS
import localconfig
from plugins.xmlsigverifyer_abstract import XmlSigVerifyerAbstract
from plugins.xmlsigverifyer_response import XmlSigVerifyerResponse
from userexceptions import *

__author__ = 'r2h2'

# style sheet to filter ds:Signature elements
xslt_str = """<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="node() | @*"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="ds:Signature"/>
</xsl:stylesheet>
"""

class XmlSigVerifyerMoasp(XmlSigVerifyerAbstract):
    """ Python wrapper for the PvzdVerifySig Java class """
    def __init__(self):
        self.pywrapper = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')

    def verify(self, xml_file_name) -> str:
        """ verify xmldsig and return signerCertificate """
        pvzdverifysig = self.pywrapper(
            os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
            os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
            xml_file_name)
        response  = pvzdverifysig.verify()
        if response.pvzdCode != 'OK':
            raise ValidationError("Signature verification failed, code=" +
                                  response.pvzdCode + "; " + response.pvzdMessage)

        # One should follow "see-what-you-signed" -> W3C XMLDsig Recommendenations
        # MOA-SP does not return (?) signed data, hence we try to remove the ds:Signature element
        # for enveloped signatures (ds:Signature is not root) from the input using a style sheet :-(
        in_dom = ET.parse(xml_file_name)
        if in_dom.getroot().tag == '{http://www.w3.org/2000/09/xmldsig#}Signature':  # don't touch enveloping ones
            with open(xml_file_name) as fd:
                signed_data_str = fd.read()
        else:
            xslt = ET.fromstring(xslt_str)
            transform = ET.XSLT(xslt)
            out_dom = transform(in_dom)
            signed_data_bytes = ET.tostring(out_dom,
                                            xml_declaration=True,
                                            encoding=localconfig.XML_ENCODING)
            signed_data_str = signed_data_bytes.decode(localconfig.XML_ENCODING)

        r = XmlSigVerifyerResponse(signed_data_str, response.signerCertificateEncoded)
        return r
