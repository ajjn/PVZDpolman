import base64, hashlib, sys
import logging
import simplejson as json
from json2html import *
from inputrecord import InputRecord
from contentrecord import ContentRecord
from wrapperrecord import WrapperRecord
from userexceptions import *
from datetime import datetime
__author__ = 'r2h2'
assert sys.version_info >= (3,4), 'modules used here support unicode and require python 3. Tested version is 3.4.3'

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
            logging.error('could not read inputfile, because: %s' %(repr(e)))
            sys.exit(1)
        self.args.input.close()
        try:
            appendList = json.loads(inputdataJSON)
        except Exception as e:
            raise JSONdecodeError
        if not isinstance(appendList, list):
            raise PMPInputRecNoDictError('JSON input file must contain a list of dict')
        if len(appendList) == 0:
            raise PMPInputRecNoDictError('JSON input file must contain a non-empty list of dict')
        if not isinstance(appendList[0], dict):
            raise PMPInputRecNoDictError('JSON input file: first object in list is not a dict')
        self.aods = self.aodsFileHandler.readFile() # does validation as well
        inputRecSeq = 0
        for inputDataRaw in appendList:
            inputRec = InputRecord(inputDataRaw)
            wrapperRec = WrapperRecord('elements', inputRec, self.args)
            inputRecSeq += 1
            policyDict = self.aods_read()  # get latest version
            logging.debug("%d rectype=%s pk=%s" % (inputRecSeq, inputRec.rec.rectype, inputRec.rec.primarykey))
            inputRec.validate(policyDict)
            lastHash = self.aods['AODS'][self.lastSeq][0]
            logging.debug("%d lastHash: " % inputRecSeq + lastHash)
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
        logging.debug("0 seedVal: " + seedVal_bytes.decode('ascii'))
        self.aodsFileHandler.create({"AODS": [wrapperRec.getRec(0, seedVal_bytes.decode('ascii'))]}, self.args.xmlsign)

    def aods_read(self) -> dict:
        '''   read aods from input file and transform into policyDict structure
              option: output policiy directory or journal in various formats
        '''
        if not hasattr(self, 'aods'):
            self.aods = self.aodsFileHandler.readFile()
        if self.aods['AODS'][0][3][0] != 'header':
            raise ValidationError('Cannot locate aods header record')
        policyDict = {"domain": {}, "issuer": {}, "organization": {}, "revocation": {}, "userprivilege": {}}
        if getattr(self.args, 'journal', False):
            output = sys.stdout if self.args.output is None else self.args.output
            output.write('[\n')
        for w in self.aods['AODS']:
            if getattr(self.args, 'journal', False):
                output.write(json.dumps(w) + '\n')
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
                    raise HashChainError('Inconsistent (AODS) data structure: deleting record without previous entry: ' + rec.rectype + ', ' + rec.primarykey)
            else:
                try:
                    policyDict[rec.rectype].update({rec.primarykey: rec.attr})
                except KeyError as e:
                    logging.error(str(wrap) + ' ' + str(rec), file=sys.stderr)
                    raise e
        if getattr(self.args, 'journal', False):
            output.write(']')
            output.close()
        if getattr(self.args, 'poldirhtml', False):
            output = sys.stdout if self.args.output is None else self.args.output
            html = '<html><head><meta charset="UTF-8"><link rel="stylesheet" type="text/css" href="../tables.css"></head><body><h1>PVZD Policy Directory</h1>%s</body></html>'
            tabhtml = json2html.convert(json=policyDict, table_attributes='class="pure-table"')
            output.write(html % tabhtml)
            output.close()
        if getattr(self.args, 'poldirjson', False):
            output = sys.stdout if self.args.output is None else self.args.output
            output.write(json.dumps(policyDict, sort_keys=True, indent=2, separators=(', ', ': ')))
            output.close()
        return policyDict

    def aods_scratch(self):
        self.aodsFileHandler.removeFile()