from __future__ import print_function
from aodsFileHandler import *
from aodsRecord import *
from userExceptions import *
__author__ = 'r2h2'


class RecordWrapper():
    ''' Handle a single wrapper-structure elements: create an object and access the attributes
        A Record wrapper is the list element that provides the hash chain, sequence number and delete flag
        around content records
    '''
    def __init__(self, rawStruct):
        try:
            self.hash = rawStruct[0]
            self.seq = rawStruct[1]
            self.deleteflag = rawStruct[2]
            self.record = rawStruct[3]
        except Exception, e:
            print(str(self), file=sys.stderr)
            raise e

    def validateWrap(self, prevHash):
        ''' validate hash chain
        :param prevHash: hash value of previous record in aods
        :return: True if valid
        '''
        wrapStruct = [self.hash, self.seq, self.deleteflag, self.record]
        digestInput = prevHash + json.dumps(wrapStruct[1:], separators=(',', ':'))
        digest = base64.b64encode(hashlib.sha256(digestInput.encode('UTF-8')).digest())
        return (digest == self.hash)

    def __str__(self):
        return str(self.seq) + ' ' + self.hash


class AodsList():
    ''' The append-only data structure is agnostic of the record type, which is defined in aodsStruct. Its primitives
        are create, append and read.
        the read function will transform it into the policyDict structure.
    '''
    def __init__(self, verbose):
        self._verbose = verbose
        self._lastSeq = None
        self._lastHash = None
        self._prevHash = None

    def aods_append(self, aodsHandler, inputfile, trustedcerts=None, xmlsign=False):
        '''
        :param aodsHandler:
        :param inputfile: arrray of records.
        :param trustedcerts: need to verify the existing AODS
        :param xmlsign: indicate whether new file will be signed
        '''
        try:
            inputdataJSON = inputfile.read()
        except (OSError, IOError) as e:
            print('could not read inputfile, because: %s' %(repr(e)))
            sys.exit(1)
        try:
            appendList = json.loads(inputdataJSON)
        except Exception, e:
            print("reading from " + inputfile.name)
            raise JSONdecodeError
        self.aods = aodsHandler.readFile() # does validation as well
        for inputDataRaw in appendList:
            appendData = InputRecord(inputDataRaw)
            if self._verbose: print("input: rectype=%s pk=%s" % (appendData.rec.rectype, appendData.rec.primarykey))
            policyDict = self.aods_read(None)
            appendData.validate(policyDict)
            lastHash = self.aods['AODS'][self._lastSeq][0]
            self.aods['AODS'].append(appendData.makeWrap(self._lastSeq + 1, lastHash, self._verbose))
        aodsHandler.save(self.aods, xmlsign)

    def aods_create(self, aodsHandlder, xmlsign=False):
        initRecord = InitRecord()
        aodsHandlder.create({"AODS": [initRecord.creatInitRec()]}, xmlsign)

    def aods_read(self, aodsHandlder, trustedcerts=None, jsondump=False, output=None):
        '''   read aods from input file and transform into policyDict structure
              if no aodsHandler is given, then the aods is already loaded  (used to refresh the dictionary)
        '''
        if not hasattr(self, 'aods'):
            self.aods = aodsHandlder.readFile()
        assert self.aods['AODS'][0][3][0] == 'header', 'Cannot locate aods header record'
        policyDict = {"domain": {}, "organization": {}, "userprivilege": {}}
        for w in self.aods['AODS']:
            wrap = RecordWrapper(w)
            rec = Record(wrap.record)
            self._prevHash = self._lastHash
            self._lastHash = wrap.hash
            self._lastSeq = wrap.seq
            if rec.rectype == 'header':
                continue
            if wrap.validateWrap(self._prevHash) != True:
                raise HashChainError('AODS hash chain is broken -> data not trustworthy, revert to previous version')
            if wrap.deleteflag:
                try:
                    del policyDict[rec.rectype][rec.primarykey]
                except KeyError:
                    print("Broken (AODS) data structure: deleting record without previous entry", file=sys.stderr)
                    sys.exit(1)
            else:
                try:
                    policyDict[rec.rectype].update({rec.primarykey: rec.attr})
                except KeyError, e:
                    print(str(wrap) + ' ' + str(rec), file=sys.stderr)
                    raise e
        if jsondump:
            output = sys.stdout if output is None else output
            output.write(json.dumps(policyDict, sort_keys=True, indent=2, separators=(', ', ': ')))
        return policyDict

    def aods_scratch(self, aodsHandlder):
        aodsHandlder.removeFile()
