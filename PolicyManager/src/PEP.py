import git
from os import path
from jnius import autoclass
from invocation import *
from aodsListHandler import *
from aodsFileHandler import *
from constants import *
from gitHandler import GitHandler
__author__ = 'r2h2'

class PEP:
    ''' The PEP (Policy Enforcement Point) performs for each invocation:
        with a well-known git location:
        for each XML file in the directory containing requests:
            check if it conforms to the policy
            if it is OK, move it to the "accepted" directory
            else move it to the "rejected" directory

        Policy check includes these policies:
            valid SAML EntityDescriptor (XSD conformance)
            valid SAML EntityDescriptor  (profile XSLT conformance)
            valid XML signature on EntityDescriptor element
            signing certificate in the policy directory
            signer authorized to use domain names in entityID, endpoints and certificate CN
            certificated is not blacklisted
    '''

    def __init__(self):
        projdir_rel = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.projdir_abs = os.path.abspath(projdir_rel)

    def isDeletionRequest(self, filename_abs):
        return os.path.getsize(filename_abs) == 0    # TODO: replace with test for signed request with custom delete attribute

    def getPolicyDict(self, invocation) -> dict:
        aodsFileHandler = AODSFileHandler(invocation)
        aodsListHandler = AodsListHandler(aodsFileHandler, invocation.args)
        return aodsListHandler.aods_read()

    def validateXSD(self, filename_abs):
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
        assert policyDict["userprivilege"].get(signerCert, None) != None, 'Signer certificate not found in policy directory'
        org_id = policyDict["userprivilege"][signerCert][0]
        allowedDomains = []
        for dn in pd["domain"].keys():
            if pd["domain"][dn][0] == org_id:
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

    def validateDomainNames(self, filename_abs, allowedDomains):
        print('allowed domains: ' + ', '.join(allowedDomains))
        return True

    def getCerts(self):
        pass  # TODO implement

    def checkCerts(self):
        for cert_pem in self.getCerts():
            cert = X509cert(cert_pem)
            assert cert.isNotExpired(), 'certificate has a notValidAfter date in the past'
            assert cert.getIssuer_str in VALIDCERTISSUERS, 'certificate was not issuer by a accredited CA'




def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    pep = PEP()
    policyDict = pep.getPolicyDict(invocation)
    gitHandler = GitHandler(invocation.args.pubrequ, invocation.args.verbose)
    for filename in gitHandler.getRequestQueueItems():
        filename_abs = invocation.args.pubrequ + '/' + filename
        filename_base = os.path.basename(filename)
        try:
            if invocation.args.verbose: print('\n== processing ' + filename_base)
            if pep.isDeletionRequest(filename_abs):
                gitHandler.remove_from_accepted(filename)
            else:
                if invocation.args.verbose: print('validating XML schema')
                pep.validateXSD(filename_abs)
                pep.validateSchematron(filename_abs)
                if invocation.args.verbose: print('validating signature')
                signerCert = pep.validateSignature(filename_abs)
                if invocation.args.verbose: print('validating signer cert, loading allowed domains')
                pep.getAllowedDomains(signerCert, policyDict)
                if invocation.args.verbose: print('validating signer\'s privileges to use domain names in URLs')
                pep.validateDomainNames(filename_abs, policyDict)
                if invocation.args.verbose: print('validating certificate(s) not expired or blacklisted and issuer is valid ')
                pep.checkCerts(filename_abs, policyDict)
            gitHandler.move_to_accepted(filename)
        except AssertionError as e:
            if invocation.args.verbose: print(str(e))
            gitHandler.move_to_rejected(filename)
            gitHandler.add_reject_message(filename_base, str(e))


if __name__ == '__main__':
    run_me()
