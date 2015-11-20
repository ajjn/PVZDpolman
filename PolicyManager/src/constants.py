import os
__author__ = 'r2h2'

GIT_REQUESTQUEUE = 'request_queue'
GIT_ACCEPTED = 'accepted'
GIT_REJECTED = 'rejected'

VALIDCERTISSUERS_IDP = [
    'C=AT, ST=Wien, O=Bundesministerium fuer Inneres, OU=IT-MS, CN=Portalverbund-CA/emailAddress=bmi-iv-2-e-ca@bmi.gv.at',
]
VALIDCERTISSUERS_SP = VALIDCERTISSUERS_IDP + []
VALIDCERTISSUERS = {'IDP': VALIDCERTISSUERS_SP, 'SP': VALIDCERTISSUERS_SP}

DATA_HEADER_B64BZIP = '{signed data format: base64(bzip2)}\n'

PROJDIR_REL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJDIR_ABS = os.path.abspath(PROJDIR_REL)

#XML namespaces for etree
XMLNS_MD = '{urn:oasis:names:tc:SAML:2.0:metadata}'