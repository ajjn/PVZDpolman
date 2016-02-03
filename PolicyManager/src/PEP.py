import git
import logging
import logging.config
import os
import re
import sys
import signxml
#from os import path
from urllib.parse import urlparse
from lxml import etree as ET
from OpenSSL import crypto
from aodsfilehandler import AODSFileHandler
from aodslisthandler import AodsListHandler
from constants import LOGLEVELS, PROJDIR_ABS, XMLNS_MD
from githandler import GitHandler
from invocation import CliPepInvocation
import loggingconfig
from samlentitydescriptor import SAMLEntityDescriptor
from userexceptions import UnauthorizedSignerError, ValidationError
from xmlsigverifyer import XmlSigVerifyer
from xy509certstore import Xy509certStore
from xy509cert import XY509cert

__author__ = 'r2h2'

class PEP:
    """ The PEP (Policy Enforcement Point) performs for each invocation:
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
    """

    def __init__(self, cliClient):
        self.projdir_abs = PROJDIR_ABS
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

    def validateSignature(self, filename_abs) -> str:
        # verify whether the signature is valid
        xml_sig_verifyer = XmlSigVerifyer();
        signerCertificateEncoded = xml_sig_verifyer.verify(filename_abs)
        #if self.verbose:
        #    cert = XY509cert(signerCertificateEncoded, inform='DER') # TODO: check encoding
        #    print('Subject CN: ' + cert.getIssuer_str)
        return signerCertificateEncoded

    def getOrgID(self, signerCert, policyDict) -> str:
        """ return associated organizazions for signer. There are two possible paths:
                signer-cert -> portaladmin -> org
                signer-cert -> identity-link/ssid -> portaladmin -> org (not implemented)
        """
        try:
            org_id = policyDict["userprivilege"]['{cert}'+signerCert][0]
        except KeyError:
            raise UnauthorizedSignerError('Signer certificate not found in policy directory')
        return org_id

    def getAllowedDomainsForOrg(self, org_id, policyDict) -> list:
        """ return allowed domains for signer. There are two possible paths:
                signer-cert -> portaladmin -> org -> domain
                signer-cert -> identity-link/ssid -> portaladmin -> org -> domain (not implemented)
        """
        allowedDomains = []
        for dn in policyDict["domain"].keys():
            if policyDict["domain"][dn][0] == org_id:
                allowedDomains.append(dn)
        return allowedDomains

    def isInAllowedDomains(self, dn, allowedDomains) -> bool:
        """  check if dn is identical to or an immediate sub-domain of an allowed domain """
        parent_dn = re.sub('^[^\.]+\.', '', dn)
        if dn in allowedDomains or parent_dn in allowedDomains:
            return True
        return False

    # removed, only accepting enveloping signatures
    # def getEntityDescriptor(self, filename_abs):
        #     """ extract the contents of the enveloping signature in filename_abs and uncompress and decode it """
    #     tree = ET.parse(filename_abs)
    #     content = tree.findtext('{http://www.w3.org/2000/09/xmldsig#}Object')
    #     if len(content) == 0:
    #         raise ValidationError('EntityDescriptor contained in XML signature value is empty')
    #     logging.debug('Found dsig:SignatureValue/text() in aods:\n%s\n' % content)
    #     content_body = re.sub(DATA_HEADER_B64BZIP, '', content)
    #     return bz2.decompress(base64.b64decode(content_body))

    def validateDomainNames(self, ed, allowedDomains) -> bool:
        """ check that entityId and endpoints contain only hostnames from allowed domains"""
        if ed.dom.tag != XMLNS_MD + 'EntityDescriptor':
            raise MissingRootElemError('Request object must contain EntityDescriptor as root element')
        entityID_url = ed.dom.attrib['entityID']
        entityID_hostname = urlparse(entityID_url).hostname
        if not self.isInAllowedDomains(entityID_hostname, allowedDomains):
            raise InvalidFQDNError('FQDN of entityID %s not in allowed domains: %s' % (entityID_hostname, allowedDomains))
        logging.debug('signer is allowed to use %s as entityID' % entityID_hostname)
        for element in ed.dom.xpath('//@location'):
            location_hostname = urlparse(element.attrib['Location']).hostname
            if self.isInAllowedDomains(location_hostname, allowedDomains):
                raise InvalidFQDNError('%s in %s not in allowed domains: %s' % (location_hostname, element.tag, allowedDomains))
            logging.debug('signer is allowed to use %s in %' % (location_hostname, element.tag.split('}')))
        return True

    def getCerts(self, ed, role) -> list:
        certs = []
        if role == 'IDP': xp = 'md:IDPSSODescriptor//ds:X509Certificate'
        if role == 'SP': xp = 'md:SPSSODescriptor//ds:X509Certificate'
        i = 0
        for elem in ed.dom.xpath(xp, namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#',
                                                  'md': 'urn:oasis:names:tc:SAML:2.0:metadata'}):
            certs.append(elem.text)
            i += 1
        return certs

    def checkCerts(self, ed, IDP_trustStore, SP_trustStore):
        """ validate that included signing and encryption certificates meet
            all of the following conditions:
            * not expired
            * issued by a CA listed as issuer in the related trust store
        """
        for cert_pem in self.getCerts(ed, 'IDP'):
            cert = XY509cert(cert_pem)
            if not cert.isNotExpired():
                raise CertExpiredError('certificate has a notValidAfter date in the past')
            x509storeContext = crypto.X509StoreContext(IDP_trustStore.x509store, cert.cert)
            try:
                x509storeContext.verify_certificate()
            except crypto.X509StoreContextError as e:
                raise CertInvalidError(('Invalid certificate. Issuer not in policy directory: ' + cert.getIssuer_str()))

        for cert_pem in self.getCerts(ed, 'SP'):
            cert = XY509cert(cert_pem)
            if not cert.isNotExpired():
                raise CertExpiredError('certificate has a notValidAfter date in the past')
            x509storeContext = crypto.X509StoreContext(SP_trustStore.x509store, cert.cert)
            x509storeContext.verify_certificate()



def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        # CLI args and logger set by unit test
        invocation = testrunnerInvocation
        exception_lvl = LOGLEVELS['DEBUG']
    else:
        invocation = CliPepInvocation()
        logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
        logging_config = loggingconfig.LoggingConfig(logbasename,
                                                     console=False,
                                                     file_level=invocation.args.loglevel)
        exception_lvl = LOGLEVELS['ERROR']

    pep = PEP(invocation)
    try:
        policyDict = pep.getPolicyDict(invocation)
    except ValidationError as e:
        logging.log(exception_lvl, str(e) + '\nterminating PEP.')
        raise
    logging.debug('initialize IDP CA certs')
    IDP_trustStore = Xy509certStore(policyDict, 'IDP')
    logging.debug('initialize SP CA certs')
    SP_trustStore = Xy509certStore(policyDict, 'SP')
    logging.debug('   using repo ' + invocation.args.pubrequ)
    gitHandler = GitHandler(invocation.args.pubrequ, verbose=invocation.args.verbose)
    for filename in gitHandler.getRequestQueueItems():
        if not filename.endswith('.xml'):
            logging.debug('   not .xml: ignoring ' + filename)
            continue
        filename_abs = invocation.args.pubrequ + '/' + filename
        filename_base = os.path.basename(filename)
        pep.file_counter += 1
        try:
            logging.debug('== processing ' + filename_base)
            if pep.isDeletionRequest(filename_abs):
                gitHandler.remove_from_accepted(filename)
            else:
                logging.debug('validating XML schema')
                with open(filename_abs) as f:
                    ed = SAMLEntityDescriptor(f)
                ed.validate_xsd()
                ed.validate_schematron()
                logging.debug('validating signature')
                signerCert = pep.validateSignature(filename_abs)
                logging.debug('validating signer cert, loading allowed domains')
                org_id = pep.getOrgID(signerCert, policyDict)
                logging.debug('validating signer\'s privileges to use domain names in URLs')
                allowedDomains = pep.getAllowedDomainsForOrg(org_id, policyDict)
                pep.validateDomainNames(ed, allowedDomains)
                logging.debug('validating certificate(s): not expired & not blacklisted & issuer is valid ')
                pep.checkCerts(ed, IDP_trustStore, SP_trustStore)
            gitHandler.move_to_accepted(filename)
            pep.file_counter_accepted += 1
        except (ValidationError, signxml.InvalidInput) as e:
            logging.log(exception_lvl, str(e))
            gitHandler.move_to_rejected(filename)
            pep.file_counter_rejected += 1
            gitHandler.add_reject_message(filename_base, str(e))
    logging.log(exception_lvl, 'files in request queue processed: ' + str(pep.file_counter) + \
                     '; accepted: ' + str(pep.file_counter_accepted) + \
                     '; rejected: ' + str(pep.file_counter_rejected) + '.')


if __name__ == '__main__':
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or greater"
    run_me()
