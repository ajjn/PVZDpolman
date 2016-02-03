import base64, bz2, sys
import logging
#from xml.etree import ElementTree
from lxml import etree as ElementTree
from signxml import *
from constants import DATA_HEADER_B64BZIP
import localconfig

__author__ = 'r2h2'

def cre_signedxml_signxml(sig_data, sig_type='envelopingB64BZIP', sig_position=None, verbose=False):
    ''' Create XML signature using py signxml (based on lxml + openssl) '''
    with open(localconfig.SIGNCERT) as fd:
        cert = fd.read()
    with open(localconfig.SIGNKEY) as fd:
        key = fd.read().encode('ascii')

    if sig_type == 'envelopingB64BZIP':
        dataObject = DATA_HEADER_B64BZIP + \
                     base64.b64encode(bz2.compress(sig_data.encode('utf-8'))).decode('ascii')
        logging.debug('data to be signed:\n%s\n\n' % dataObject)
        signed_root = xmldsig(dataObject).sign(method=methods.enveloping, key=key, cert=cert)
    elif sig_type == 'enveloped':
        root = ElementTree.fromstring(sig_data)
        signed_root = xmldsig(root).sign(method=methods.enveloped, key=key, cert=cert)
        #verified_data = xmldsig(signed_root).verify()
    else:
        raise ValidationError("Signature type must be one of 'envelopingB64BZIP', 'enveloped' but is " + sig_type)

    #xml_str = ElementTree.dump(signed_root)
    xml_bytes = ElementTree.tostring(signed_root, xml_declaration=True, encoding='utf-8')
    xml_str = xml_bytes.decode('utf-8')
    return xml_str