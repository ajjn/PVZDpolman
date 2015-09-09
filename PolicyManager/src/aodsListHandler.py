from __future__ import print_function
import sys
import simplejson as json
import base64, hashlib
from inputRecord import InputRecord
from contentRecord import ContentRecord
from wrapperRecord import WrapperRecord
from userExceptions import *
from datetime import datetime
__author__ = 'r2h2'


class AodsListHandler:
    ''' The append-only data structure is agnostic of the record type, which is defined in as content record. Its
        primitives are create, append and read and scretch.
        The read function will transform it into the policyDict structure.
    '''

    def __init__(self, aodsFileHandler, args):
        self.aodsFileHandler = aodsFileHandler
        self.args = args
        self.lastSeq = None
        self.lastHash = None
        self.prevHash = None

    def aods_append(self):
        try:
            inputdataJSON = self.args.input.read()
        except (OSError, IOError) as e:
            print('could not read inputfile, because: %s' %(repr(e)))
            sys.exit(1)
        try:
            appendList = json.loads(inputdataJSON)
        except Exception:
            print("reading from " + self.args.input.name)
            raise JSONdecodeError
        self.aods = self.aodsFileHandler.readFile() # does validation as well
        inputRecSeq = 0
        for inputDataRaw in appendList:
            inputRec = InputRecord(inputDataRaw)
            wrapperRec = WrapperRecord('elements', inputRec, self.args)
            inputRecSeq += 1
            policyDict = self.aods_read()  # get latest version
            if self.args.verbose: print("aods_append: %d rectype=%s pk=%s" % (inputRecSeq, inputRec.rec.rectype, inputRec.rec.primarykey))
            inputRec.validate(policyDict)
            lastHash = self.aods['AODS'][self.lastSeq][0]
            if self.args.verbose: print("aods_append %d lastHash: " % inputRecSeq + lastHash)
            wrapperRec_final = wrapperRec.getRec(self.lastSeq + 1, lastHash)
            self.aods['AODS'].append(wrapperRec_final)
        self.aodsFileHandler.save(self.aods, self.args.xmlsign)

    def aods_create(self):
        inputDataRaw = {"record": ["header", "", "columns: hash, seq, delete, [rectype, pk, a1, a2, ..], datetimestamp, registrant, submitter]" ], "delete": False}
        inputRec = InputRecord(inputDataRaw)
        wrapperRec = WrapperRecord('elements', inputRec, self.args)
        seedVal_str = str(datetime.now())
        seedVal_bytes = base64.b64encode(hashlib.sha256(seedVal_str.encode('ascii')).digest())
        if self.args.debug: seedVal_bytes = 'fixedValueForDebugOnly'.encode('ascii')
        if self.args.verbose: print("aods_create: 0 seedVal: " + seedVal_bytes.decode('ascii'))
        self.aodsFileHandler.create({"AODS": [wrapperRec.getRec(0, seedVal_bytes.decode('ascii'))]}, self.args.xmlsign)

    def aods_read(self) -> dict:
        '''   read aods from input file and transform into policyDict structure  '''
        if not hasattr(self, 'aods'):
            self.aods = self.aodsFileHandler.readFile()
        assert self.aods['AODS'][0][3][0] == 'header', 'Cannot locate aods header record'
        policyDict = {"domain": {}, "organization": {}, "userprivilege": {}}
        for w in self.aods['AODS']:
            wrap = WrapperRecord('rawStruct', w, self.args)
            rec = ContentRecord(wrap.record)
            self.prevHash = self.lastHash
            self.lastHash = wrap.hash
            self.lastSeq = wrap.seq
            if rec.rectype == 'header':
                continue
            if wrap.validateWrap(self.prevHash) != True:
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
                except KeyError as e:
                    print(str(wrap) + ' ' + str(rec), file=sys.stderr)
                    raise e
        if getattr(self.args, 'jsondump', False):
            output = sys.stdout if self.args.output is None else self.args.output
            output.write(json.dumps(policyDict, sort_keys=True, indent=2, separators=(', ', ': ')))
            output.close()
        return policyDict

    def aods_scratch(self):
        self.aodsFileHandler.removeFile()
