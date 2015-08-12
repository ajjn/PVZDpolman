from __future__ import print_function
import base64, datetime, hashlib, os, sys
from aodsStruct import *
from userExceptions import *
from creSignedXML import creSignedXML
from jnius import autoclass
import xml.etree.ElementTree as ET
__author__ = 'r2h2'


class AODSFileHandler():
    def __init__(self, cliClient):
        self._aodsFile = cliClient.args.aods
        if cliClient.args.xmlsign and self._aodsFile[-4:] != '.xml':
            self._aodsFile += '.xml'
        if not cliClient.args.xmlsign and self._aodsFile[-5:] != '.json':
            self._aodsFile += '.json'
        self.trustCertsFile = os.path.abspath(cliClient.args.trustedcerts)

    def create(self, s, xmlsign):
        if os.path.exists(self._aodsFile):
            print('Must remove existing %s before creating a new AODS' % self._aodsFile)
            sys.exit(1)
        f = open(self._aodsFile, 'w')
        if xmlsign:
            f.write(creSignedXML(json.dumps(s)))
        else:
            f.write(json.dumps(s))

    def readFile(self):
        if self._aodsFile[-4:] == '.xml':
            PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.PvzdVerfiySig');
            verifier = PvzdVerfiySig(
                "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
                "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties",
                "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata/idp5_valid.xml_sig.xml")
            response  = verifier.verify()
            assert 'OK' == response.pvzdCode
                   #, "Signature verification failed, code=" + response.pvzdCode + "; " + response.pvzdMessage
            trustCerts = json.loads(open(self.trustCertsFile).read())
            assert response.signerCertificateEncoded in trustCerts #,                   "Signature certificate not in trusted list. Signature cert is\n" + response.signerCertificateEncoded
            tree = ET.parse(self.trustCerts)
            sigval = tree.find('{http://www.w3.org/2000/09/xmldsig#}SignatureValue').text
            assert len(sigval) > 0, "AODS contained in XML signature value is empty"
            return sigval
        else:  # must be json
            f = open(self._aodsFile, 'r')
            return json.loads(f.read())

    def removeFile(self):
        ''' remove file but ignore if it does not exist '''
        try:
            os.remove(self._aodsFile)
        except OSError, e:
            if e.errno != 2:
                raise e

    def save(self, s, xmlsign):
        f = open(self._aodsFile, 'w')
        f.truncate()
        if xmlsign:
            f.write(creSignedXML(json.dumps(s)))
        else:
            f.write(json.dumps(s))


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
        :param prevHash: hash value of previous record in aods
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

    def aods_append(self, aodsHandler, inputfile, trustedcerts, xmlsign=False):
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
        directory = self.aods_read(aodsHandler, trustedcerts) # does validation as well
        appendData.validate(directory)
        aods = aodsHandler.readFile()
        lastHash = aods['AODS'][self._lastSeq][0]
        aods['AODS'].append(appendData.makeWrap(self._lastSeq + 1, lastHash, self._verbose))
        aodsHandler.save(aods, xmlsign)

    def aods_create(self, aodsHandlder, xmlsign=False):
        initRecord = InitRecord()
        aodsHandlder.create({"AODS": [initRecord.creatInitRec()]}, xmlsign)

    def aods_read(self, aodsHandlder, trustedcerts, jsondump=False, output=None):
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
