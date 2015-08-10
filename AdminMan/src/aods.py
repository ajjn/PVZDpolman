from __future__ import print_function
import base64, datetime, hashlib, os, sys
from aodsStruct import *
from userExceptions import *
__author__ = 'r2h2'


class AODSFileHandler():
    def __init__(self, cliClient):
        self._aodsFile = cliClient.args.aods

    def create(self, s):
        if os.path.exists(self._aodsFile):
            print('Must remove existing %1 before creating a new AODS')
            sys.exit(1)
        _f = open(self._aodsFile, 'w')
        _f.write(json.dumps(s))

    def readFile(self):
        _f = open(self._aodsFile, 'r')
        return json.loads(_f.read())

    def removeFile(self):
        ''' remove file but ignore if it does not exist '''
        try:
            os.remove(self._aodsFile)
        except OSError, e:
            if e.errno != 2:
                raise e

    def save(self, s):
        _f = open(self._aodsFile, 'w')
        _f.truncate()
        _f.write(json.dumps(s))


class WrapStruct():
    ''' Handle a single wrapper-structure elements: create an object and access the attributes '''
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
        :param lastHash: hash value of previous record in aods
        :param verbose: boolean
        :return: True if valid
        '''
        wrapStruct = [self.hash, self.seq, self.deleteflag, self.record]
        digestInput = prevHash + json.dumps(wrapStruct[1:], separators=(',', ':'))
        digest = base64.b64encode(hashlib.sha256(digestInput).digest())
        return (digest == self.hash)

    def __str__(self):
        return str(self.seq) + ' ' + self.hash


class InitRecord():
    ''' Define the header record '''
    def creatInitRec(self):
        _seedVal = base64.b64encode(hashlib.sha256(str(datetime.datetime.now())).digest())
        return [_seedVal, 0, False, ["header", "", "columns: hash, seq, delete, [rectype, pk, a1, a2, ..]]" ]]


class AODS():
    ''' The append-only data structure is agnostic of the record type, which is defined in aodsStruct. Its primitives
        are create, append and read.
    '''
    def __init__(self, verbose):
        self._verbose = verbose
        self._lastSeq = None
        self._lastHash = None
        self._prevHash = None

    def aods_append(self, aodsHandler, inputfile):
        try:
            inputdataJSON = inputfile.read()
        except (OSError, IOError) as e:
            print('could not read inputfile, because: %s' %(repr(e)))
            sys.exit(1)
        try:
            inputDataRaw = json.loads(inputdataJSON)
        except Exception, e:
            raise JSONdecodeError
        appendData = AppendRecord(inputDataRaw)
        if self._verbose: print("input: rectype=%s pk=%s" % (appendData.rectype, appendData.primarykey))
        directory = self.aods_read(aodsHandler) # does validation as well
        appendData.validate(directory)
        aods = aodsHandler.readFile()
        lastHash = aods['AODS'][self._lastSeq][0]
        aods['AODS'].append(appendData.makeWrap(self._lastSeq + 1, lastHash, self._verbose))
        aodsHandler.save(aods)

    def aods_create(self, aodsHandlder):
        initRecord = InitRecord()
        aodsHandlder.create({"AODS": [initRecord.creatInitRec()]})

    def aods_read(self, aodsHandlder, jsondump=False, output=None):
        '''   read aods from input file and transform into directory structure '''
        aods = aodsHandlder.readFile()
        assert aods['AODS'][0][3][0] == 'header', 'Cannot locate aods header record'
        directory = {"domain": {}, "organization": {}, "userprivilege": {}}
        for w in aods['AODS']:
            wrap = WrapStruct(w)
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
                    del directory[rec.rectype][rec.primarykey]
                except KeyError:
                    print("Broken (AODS) data structure: deleting record without previous entry", file=sys.stderr)
                    sys.exit(1)
            else:
                try:
                    directory[rec.rectype].update({rec.primarykey: rec.attr})
                except KeyError, e:
                    print(str(wrap) + ' ' + str(rec), file=sys.stderr)
                    raise e
        if jsondump:
            output = sys.stdout if output is None else output
            output.write(json.dumps(directory, sort_keys=True, indent=2, separators=(', ', ': ')))
        return directory

    def aods_scratch(self, aodsHandlder):
        aodsHandlder.removeFile()
