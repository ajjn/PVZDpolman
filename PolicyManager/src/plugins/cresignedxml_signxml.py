import base64, bz2, sys
import logging
from xml.etree import ElementTree
from signxml import xmldsig
from constants import DATA_HEADER_B64BZIP
import localconfig

__author__ = 'r2h2'

def cre_signedxml_signxml(sig_data, sig_type='envelopingB64BZIP', sig_position=None, verbose=False):
    ''' Create XML signature using py signxml (based on lxml + openssl)
    '''

    if sig_type not in ('envelopingB64BZIP', 'enveloped'):
        raise ValidationError("Signature type must be one of 'envelopingB64BZIP', 'enveloped' but is " + sig_type)
    #fail_if_securitylayer_unavailable()
    #if sigType == 'envelopingB64BZIP':
    #    dataObject = DATA_HEADER_B64BZIP + base64.b64encode(bz2.compress(data.encode('utf-8'))).decode('ascii')
    #else:
    #    dataObject = data

    logging.debug('data to be signed:\n%s\n\n' % sig_data)

    cert = open(localconfig.SIGNCERT).read()
    key = open(localconfig.SIGNKEY).read().encode('ascii')
    root = ElementTree.fromstring(sig_data)
    signed_root = xmldsig(root).sign(key=key, cert=cert)

    #return ElementTree.tostring(signed_root, encoding="utf-8")
    return ElementTree.dump(signed_root)