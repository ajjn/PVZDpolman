from __future__ import print_function
from userExceptions import *
__author__ = 'r2h2'

''' Classes in this source file encapsulate the structure of record types '''

class ContentRecord:
    ''' Handle a single content record, agnostic of the record type: create an object and access the attributes '''
    recordTypes = ["domain", "organization", "userprivilege", "header"]

    def __init__(self, rawRec):
        self.raw = rawRec
        self.rectype = rawRec[0]
        if self.rectype not in ContentRecord.recordTypes: raise InputValueError('invalid record type: %s' % self.rectype)
        self.primarykey = rawRec[1]
        self.attr = rawRec[2:]

    def validateRec(self, dir, deleteflag):
        if not isinstance(self.primarykey, str): raise InputFormatError('primary key of record must be of type string')
        if self.primarykey == '': raise InputValueError('primary key of record must not be empty')
        if deleteflag and dir[self.rectype][self.primarykey] is None:
            raise InputValueError('adding delete command for non-existing record')
        if self.rectype == "domain":
            if len(self.attr) != 1: raise InputFormatError('domain record must have exactly 1 attribute (the org-id)')
            if not isinstance(self.attr[0], str):
                raise InputFormatError('org-id (first attribute of domain record) must be of type string')
            if self.attr[0] not in dir['organization']:
                raise InputValueError('adding domain record referencing non-existing organization, orgid = %s' % self.attr[0])
        elif self.rectype == "organization":
            if len(self.attr) != 1:
                raise InputFormatError('organization record must have exactly 1 attribute (the org-id)')
            if not isinstance(self.attr[0], str):
                raise InputFormatError('org-name (first attribute of organization record) must be of type string')
        elif self.rectype == "userprivilege":
            #if self.primarykey[0:6] not in ('cert', '{ssid}'):
                # raise InputFormatError('primary key of userprivilege must start with {cert} or {ssid}') # bPK (=ssid) not implemented
            if self.primarykey[0:6] != '{cert}':
                raise InputFormatError('primary key of userprivilege must start with {cert}')
            if len(self.attr) != 2:
                raise InputFormatError('user privilege record must have 2 attributes (org-id, name')
            if not isinstance(self.attr[0], str):
                raise InputFormatError('org-id (first attribute of user privilege record) must be of type string')
            if not isinstance(self.attr[1], str):
                raise InputFormatError('cert (2nd attribute of user privilege record) must be of type string')
            if self.attr[0] not in dir['organization']:
                raise InputValueError('adding user privilege record referencing non-existing organization, pk=%s, orgid=%s' % (self.primarykey, self.attr[0]))
        elif self.rectype == "revocation":
            if len(self.attr) != 1:
                raise InputFormatError('revocation record must have exactly 1 attribute (the certificate)')
            if not isinstance(self.attr[0], str):
                raise InputFormatError('certificate (first attribute of revocation record) must be of type string')

    def __str__(self):
        return self.rectype + ' ' + self.primarykey
