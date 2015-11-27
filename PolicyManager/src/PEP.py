import git
from os import path
from urllib.parse import urlparse
from lxml import etree as ET
from jnius import autoclass
from aodsFileHandler import *
from aodsListHandler import *
from constants import *
from gitHandler import GitHandler
from invocation import *
from x509cert import X509cert
__author__ = 'r2h2'

class PEP:
    ''' The PEP (Policy Enforcement Point) performs for each invocation:
        with a well-known git location:
        for each request file in the directory containing requests:
            check if it conforms to the policy
            if it is OK, move it to the "accepted" directory
            else move it to the "rejected" directory

        A request is an enveloping signature containing an b64-encoded/zipped SAML EntityDescriptor

        Policy conformance checks includes these policies:
            on the request:
                check valid signature
                check signer's binding to policy directory (certificate or ssid)
                signing certificate in the policy directory
            on the EntityDescriptor:
                valid SAML EntityDescriptor (XSD conformance)
                valid SAML EntityDescriptor  (profile XSLT conformance)
                signer authorized to use domain names in entityID, endpoints and certificate CN
                certificated is not blacklisted, not expired and from a listed issuer
    '''

    def __init__(self,cliClient):
        projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.projdir_abs = os.path.abspath(projdir_rel)
        self.verbose = cliClient.args.verbose
        self.file_counter = 0
        self.file_counter_accepted = 0
        self.file_counter_rejected = 0

    def isDeletionRequest(self, filename_abs):
        return os.path.getsize(filename_abs) == 0    # TODO: replace with test for signed request with custom delete attribute

    def getPolicyDict(self, invocation) -> dict:
        aodsFileHandler = AODSFileHandler(invocation)
        aodsListHandler = AodsListHandler(aodsFileHandler, invocation.args)
        return aodsListHandler.aods_read()

    def validateSAMLmdXSD(self, filename_abs):
        XmlValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XmlValidator')
        validator = XmlValidator(os.path.join(self.projdir_abs, 'ValidateXSD/SAML_MD_Schema'), False)
        validator.validateSchema(filename_abs)

    def validateSchematron(self, filename_abs):
        pass  # TODO: implement

    def validateSignature(self, filename_abs) -> str:
        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
        verifier = PvzdVerfiySig(
            os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
            os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
            filename_abs)
        response = verifier.verify()
        assert 'OK' == response.pvzdCode, \
            "Signature verification failed, code=" + response.pvzdCode + "; " + response.pvzdMessage
        return response.signerCertificateEncoded

    def getAllowedDomains(self, signerCert, policyDict) -> list:
        ''' return allowed domains for signer. There are two possible paths:
                signer-cert -> portaladmin -> org -> domain
                signer-cert -> identity-link/ssid -> portaladmin -> org -> domain (not implemented)
        '''
        assert policyDict["userprivilege"].get(signerCert, None) != None, 'Signer certificate not found in policy directory'
        org_id = policyDict["userprivilege"][signerCert][0]
        allowedDomains = []
        for dn in policyDict["domain"].keys():
            if policyDict["domain"][dn][0] == org_id:
                allowedDomains.append(dn)
        return allowedDomains

    def assertNameInAllowedDomains(self, dn, allowedDomains) -> bool:
        '''  check if dn is identical to or a sub-domain of an allowed domain  '''
        isInAllowed = False
        for adn in allowedDomains:
            if dn == adn:
                isInAllowed = True
                break
        return isInAllowed

    def getEntityDescriptor(self, filename_abs):
        ''' extract the contents of the enveloping signature in filename_abs and uncompress and decode it '''
        tree = ET.parse(filename_abs)
        content = tree.findtext('{http://www.w3.org/2000/09/xmldsig#}Object')
        assert len(content) > 0, 'EntityDescriptor contained in XML signature value is empty'
        if self.verbose: print('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
        content_body = re.sub(DATA_HEADER_B64BZIP, '', content)
        return bz2.decompress(base64.b64decode(content_body))


    def validateDomainNames(self, ed_str, allowedDomains) -> bool:
        ''' check that entityId and endpoints contain only hostnames from allowed domains'''
        ed_root = ET.fromstring(ed_str)
        assert ed_root.tag == XMLNS_MD + 'EntityDescriptor', 'Request object must contain EntityDescriptor as root element'
        entityID_url = ed_root.attrib['entityID']
        entityID_hostname = urlparse(entityID_url).hostname
        assert entityID_hostname in allowedDomains, '%s not in allowed domains: %s' % (entityID_hostname, allowedDomains)
        if self.verbose: print('signer is allowed to use %s as entityID' % entityID_hostname)
        for element in ed_root.xpath('//[@location]'):
            location_hostname = urlparse(element.attrib['Location']).hostname
            assert location_hostname in allowedDomains, '%s in %s not in allowed domains: %s' % \
                                                        (location_hostname, element.tag, allowedDomains)
            if self.verbose: print('signer is allowed to use %s in %' % (location_hostname, element.tag.split('}')))
        return True

    def getCerts(self, ed_str, role) -> list:
        ed_root = ET.fromstring(ed_str)
        certs = []
        if role == 'IDP': xp = 'md:IDPSSODescriptor//ds:X509Certificate'
        if role == 'SP': xp = 'md:SPSSODescriptor//ds:X509Certificate'
        for elem in ed_root.xpath(xp, namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#',
                                                  'md': 'urn:oasis:names:tc:SAML:2.0:metadata'}):
             certs.append(self, elem.text)
        return certs

    def checkCerts(self, ed_str, role):
        ''' do certificate validation for singing and encryption certificates '''
        for cert_pem in self.getCerts(ed_str, role):
            cert = X509cert(cert_pem)
            assert cert.isNotExpired(), 'certificate has a notValidAfter date in the past'
            assert cert.getIssuer_str in VALIDCERTISSUERS[role], 'certificate was not issuer by a accredited CA'


def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    pep = PEP(invocation)
    policyDict = pep.getPolicyDict(invocation)
    if invocation.args.verbose: print('   using repo ' + invocation.args.pubrequ)
    gitHandler = GitHandler(invocation.args.pubrequ, invocation.args.verbose)
    for filename in gitHandler.getRequestQueueItems():
        if not filename.endswith('.xml'):
            if invocation.args.verbose: print('   ignoring ' + filename)
            continue
        filename_abs = invocation.args.pubrequ + '/' + filename
        filename_base = os.path.basename(filename)
        pep.file_counter += 1
        try:
            if invocation.args.verbose: print('\n== processing ' + filename_base)
            if pep.isDeletionRequest(filename_abs):
                gitHandler.remove_from_accepted(filename)
            else:
                if invocation.args.verbose: print('validating XML schema')
                pep.validateSAMLmdXSD(filename_abs)
                pep.validateSchematron(filename_abs)
                if invocation.args.verbose: print('validating signature')
                signerCert = pep.validateSignature(filename_abs)
                if invocation.args.verbose: print('validating signer cert, loading allowed domains')
                pep.getAllowedDomains(signerCert, policyDict)
                ed_str = pep.getEntityDescriptor(filename_abs)
                if invocation.args.verbose: print('validating signer\'s privileges to use domain names in URLs')
                pep.validateDomainNames(ed_str, policyDict)
                if invocation.args.verbose: print('validating certificate(s) not expired or blacklisted and issuer is valid ')
                pep.checkCerts(ed_str, 'IDP')
                pep.checkCerts(ed_str, 'SP')
            gitHandler.move_to_accepted(filename)
            pep.file_counter_accepted += 1
        except AssertionError as e:
            if invocation.args.verbose: print(str(e))
            gitHandler.move_to_rejected(filename)
            pep.file_counter_rejected += 1
            gitHandler.add_reject_message(filename_base, str(e))
    if invocation.args.verbose:
        print('files processed: ' + str(pep.file_counter) + '\n' + \
              'files accepted: ' + str(pep.file_counter_accepted) + '\n' + \
              'files rejected: ' + str(pep.file_counter_rejected) + '\n')

if __name__ == '__main__':
    run_me()
