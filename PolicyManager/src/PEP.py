import git
import logging
from os import path
from urllib.parse import urlparse
from lxml import etree as ET
from jnius import autoclass
from aodsFileHandler import *
from aodsListHandler import *
from constants import *
from gitHandler import GitHandler
from invocation import *
from SAMLEntityDescriptor import *
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

    def __init__(self, cliClient):
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

    def validateSchematron(self, filename_abs):
        pass  # TODO: implement

    def validateSignature(self, filename_abs) -> str:
        PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
        verifier = PvzdVerfiySig(
            os.path.join(PROJDIR_ABS, 'conf/moa-spss/MOASPSSConfiguration.xml'),
            os.path.join(PROJDIR_ABS, 'conf/log4j.properties'),
            filename_abs)
        response = verifier.verify()
        if response.pvzdCode != 'OK': \
            raise SignatureVerificationFailed("Signature verification failed, code=" + \
                                              response.pvzdCode + "; " + response.pvzdMessage)
        #if self.verbose:
        #    cert = X509cert(response.signerCertificateEncoded, inform='DER') # TODO: check encoding
        #    print('Subject CN: ' + cert.getIssuer_str)
        return response.signerCertificateEncoded

    def getAllowedDomains(self, signerCert, policyDict) -> list:
        ''' return allowed domains for signer. There are two possible paths:
                signer-cert -> portaladmin -> org -> domain
                signer-cert -> identity-link/ssid -> portaladmin -> org -> domain (not implemented)
        '''
        if policyDict["userprivilege"].get(signerCert, None) is None:
            raise UnauthorizedSigner( 'Signer certificate not found in policy directory')
        org_id = policyDict["userprivilege"][signerCert][0]
        allowedDomains = []
        for dn in policyDict["domain"].keys():
            if policyDict["domain"][dn][0] == org_id:
                allowedDomains.append(dn)
        return allowedDomains

    def assertNameInAllowedDomains(self, dn, allowedDomains) -> bool:
        '''  check if dn is identical to or a sub-domain of an allowed domain '''
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
        if len(content) == 0:
            raise ValidationFailure('EntityDescriptor contained in XML signature value is empty')
        logging.debug('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
        content_body = re.sub(DATA_HEADER_B64BZIP, '', content)
        return bz2.decompress(base64.b64decode(content_body))


    def validateDomainNames(self, ed_str, allowedDomains) -> bool:
        ''' check that entityId and endpoints contain only hostnames from allowed domains'''
        ed_root = ET.fromstring(ed_str)
        if ed_root.tag != XMLNS_MD + 'EntityDescriptor':
            raise MissingRootElem('Request object must contain EntityDescriptor as root element')
        entityID_url = ed_root.attrib['entityID']
        entityID_hostname = urlparse(entityID_url).hostname
        if entityID_hostname not in allowedDomains:
            raise InvalidFQDN('%s not in allowed domains: %s' % (entityID_hostname, allowedDomains))
        logging.debug('signer is allowed to use %s as entityID' % entityID_hostname)
        for element in ed_root.xpath('//[@location]'):
            location_hostname = urlparse(element.attrib['Location']).hostname
            if location_hostname not in allowedDomains:
                raise InvalidFQDN('%s in %s not in allowed domains: %s' % (location_hostname, element.tag, allowedDomains))
            logging.debug('signer is allowed to use %s in %' % (location_hostname, element.tag.split('}')))
        return True

    def getCerts(self, ed_str, role) -> list:
        ed_root = ET.fromstring(ed_str)
        certs = []
        if role == 'IDP': xp = 'md:IDPSSODescriptor//ds:X509Certificate'
        if role == 'SP': xp = 'md:SPSSODescriptor//ds:X509Certificate'
        i = 0
        for elem in ed_root.xpath(xp, namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#',
                                                  'md': 'urn:oasis:names:tc:SAML:2.0:metadata'}):
            certs.append(self, elem.text)
            i += 1
        if i == 0:
            raise EntityRoleMissingCert
        return certs

    def checkCerts(self, ed_str, role):
        ''' do certificate validation for singing and encryption certificates '''
        # TODO: prüfung auf count(certs) > 0
        for cert_pem in self.getCerts(ed_str, role):
            cert = X509cert(cert_pem)
            if not cert.isNotExpired():
                raise CertExpired('certificate has a notValidAfter date in the past')
            if cert.getIssuer_str not in VALIDCERTISSUERS[role]:
                raise CertInvalidIssuer('certificate was not issued by a accredited CA')


def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()
    projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    projdir_abs = os.path.abspath(projdir_rel)
    pep = PEP(invocation)
    policyDict = pep.getPolicyDict(invocation)
    logging.debug('   using repo ' + invocation.args.pubrequ)
    gitHandler = GitHandler(invocation.args.pubrequ, invocation.args.verbose)
    for filename in gitHandler.getRequestQueueItems():
        if not filename.endswith('.xml'):
            logging.debug('   ignoring ' + filename)
            continue
        filename_abs = invocation.args.pubrequ + '/' + filename
        filename_base = os.path.basename(filename)
        pep.file_counter += 1
        try:
            logging.debug('\n== processing ' + filename_base)
            if pep.isDeletionRequest(filename_abs):
                gitHandler.remove_from_accepted(filename)
            else:
                logging.debug('validating XML schema')
                ed = SAMLEntityDescriptor(filename_abs, projdir_abs)
                ed.validateXSD()
                pep.validateSchematron(filename_abs)
                logging.debug('validating signature')
                signerCert = pep.validateSignature(filename_abs)
                logging.debug('validating signer cert, loading allowed domains')
                pep.getAllowedDomains(signerCert, policyDict)
                ed_str = pep.getEntityDescriptor(filename_abs)
                logging.debug('validating signer\'s privileges to use domain names in URLs')
                pep.validateDomainNames(ed_str, policyDict)
                logging.debug('validating certificate(s): not expired & not blacklisted & issuer is valid ')
                pep.checkCerts(ed_str, 'IDP')
                pep.checkCerts(ed_str, 'SP')
            gitHandler.move_to_accepted(filename)
            pep.file_counter_accepted += 1
        except ValidationFailure as e:
            logging.debug(str(e))
            gitHandler.move_to_rejected(filename)
            pep.file_counter_rejected += 1
            gitHandler.add_reject_message(filename_base, str(e))
    if invocation.args.verbose:
        logging.debug('files processed: ' + str(pep.file_counter) + '\n' + \
                      'files accepted: ' + str(pep.file_counter_accepted) + '\n' + \
                      'files rejected: ' + str(pep.file_counter_rejected) + '\n')


if __name__ == '__main__':
    run_me()
