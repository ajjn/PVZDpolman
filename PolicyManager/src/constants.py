import os
__author__ = 'r2h2'

GIT_REQUESTQUEUE = 'request_queue'
GIT_ACCEPTED = 'accepted'
GIT_REJECTED = 'rejected'

VALIDCERTISSUERS = [
    '/C=IL/O=StartCom Ltd./OU=Secure Digital Certificate Signing/CN=StartCom Class 1 Primary Intermediate Server CA',
]

DATA_HEADER_B64BZIP = '{signed data format: base64(bzip2)}\n'

PROJDIR_REL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJDIR_ABS = os.path.abspath(PROJDIR_REL)