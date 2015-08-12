from __future__ import print_function
import base64, hashlib
import simplejson as json
from userExceptions import *
__author__ = 'r2h2'

''' Classes in this source file encapsulate the structure of record types '''

class Record():
    ''' Handle a single record, agnostic of the record type: create an object and access the attributes '''
    recordTypes = ["domain", "organization", "userprivilege", "header"]

    def __init__(self, rawRec):
        self.raw = rawRec
        self.rectype = rawRec[0]
        if self.rectype not in Record.recordTypes: raise InputValueError('invalid record type: %s' % self.rectype)
        self.primarykey = rawRec[1]
        self.attr = rawRec[2:]

    def validateRec(self, dir, deleteflag):
        if not isinstance(self.primarykey, basestring): raise InputFormatError('primary key of record must be of type string')
        if self.primarykey == '': raise InputValueError('primary key of record must not be empty')
        if deleteflag and dir[self.rectype][self.primarykey] is None: raise InputValueError('adding delete command for non-existing record')
        if self.rectype == "domain":
            if len(self.attr) != 1: raise InputFormatError('domain record must have exactly 1 attribute (the org-id)')
            if not isinstance(self.attr[0], basestring): raise InputFormatError('org-id (first attribute of domain record) must be of type string')
            if self.attr[0] not in dir['organization']: raise InputValueError('adding domain record referencing non-existing organization, orgid = %s' % self.attr[0])
        elif self.rectype == "organization":
            if len(self.attr) != 1: raise InputFormatError('organization record must have exactly 1 attribute (the org-id)')
            if not isinstance(self.attr[0], basestring): raise InputFormatError('org-name (first attribute of organization record) must be of type string')
        elif self.rectype == "userprivilege":
            if len(self.attr) not in range(3,5): raise InputFormatError('user privilege record must have 3 or 4 attributes (name, pubkey, role [, ssid])')
            if not isinstance(self.attr[0], basestring): raise InputFormatError('org-id (first attribute of user privilege record) must be of type string')
            if not isinstance(self.attr[1], basestring): raise InputFormatError('cert (2nd attribute of user privilege record) must be of type string')
            if not isinstance(self.attr[2], basestring): raise InputFormatError('role (3rd attribute of user privilege record) must be of type string')
            if not self.attr[2] in ('admin', 'verifier', 'manager'): raise InputFormatError('role (3rd attribute of user privilege record) must be of type string')
            if len(self.attr) == 4 and not isinstance(self.attr[3], basestring): raise InputFormatError("role must be one of 'admin', 'verifier', 'manager'")
            if self.attr[0] not in dir['organization']: raise InputValueError('adding user privilege record referencing non-existing organization, pk=%s, orgid=%s' % (self.primarykey, self.attr[0]))

    def __str__(self):
        return self.rectype + ' ' + self.primarykey


class AppendRecord():
    ''' Handle a record to be appended '''

    def __init__(self, appendData):
        assert isinstance(appendData, dict), 'input record to be appended must be of type dict'
        assert 'record' in appendData, 'input record dict must have the key "record"'
        self.rec = Record(appendData['record'])
        self.deleteflag = appendData['delete']
        assert isinstance(self.deleteflag, bool)

    def validate(self, dir):
        self.rec.validateRec(dir, self.deleteflag)

    def makeWrap(self, newSeq, lastHash, verbose):
        ''' compute hash: take last hash and append the representation of the wrapped structure
        of json.dumps in compact representaion
        :param newSeq: Sequence number to be assigned to the new record
        :param lastHash: hash value of last record in aods
        :param verbose: boolean
        :return: wrapped structure to be appended to aods including hash
        '''
        if verbose: print("lastHash: " + lastHash)
        wrapStruct = ["placeholder_for_digest", newSeq, self.deleteflag, self.rec.raw]
        digestInput = lastHash + json.dumps(wrapStruct[1:], separators=(',', ':'))
        digest = base64.b64encode(hashlib.sha256(digestInput).digest())
        return [digest] + wrapStruct[1:]
