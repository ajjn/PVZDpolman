import os
__author__ = 'r2h2'

GIT_REQUESTQUEUE = 'request_queue'
GIT_DELETED = 'deleted'
GIT_REJECTED = 'rejected'
GIT_POLICYDIR = 'policydir'
GIT_PUBLISHED = 'published'

DATA_HEADER_B64BZIP = '{signed data format: base64(bzip2)}\n'

PROJDIR_REL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJDIR_ABS = os.path.abspath(PROJDIR_REL)

#XML namespaces for etree
XMLNS_MD = '{urn:oasis:names:tc:SAML:2.0:metadata}'
XMLNS_PVZD = '{http://egov.gv.at/pvzd1.xsd}'

# loglevles valid for this project
LOGLEVELS = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10}
