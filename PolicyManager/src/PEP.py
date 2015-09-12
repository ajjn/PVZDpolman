import git
from os import path
from jnius import autoclass
from invocation import *
from aodsListHandler import *
from aodsFileHandler import *
from gitHandler import GitHandler
__author__ = 'r2h2'

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
'''


def getPolicyDict(invocation) -> dict:
    aodsFileHandler = AODSFileHandler(invocation)
    aodsListHandler = AodsListHandler(aodsFileHandler, invocation.args)
    return aodsListHandler.aods_read()


def validateXSD(filename_abs):
    XmlValidator = autoclass('at.wien.ma14.pvzd.validateXSD')
    validator = XmlValidator('ValidateXSD/SAML_MD_Schema')
    validator.validateXmlAgainstXsds(filename_abs)


def validateSchematron(filename_abs):
    pass  # TODO: implement


def validateSignature(filename_abs) -> str:
    PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.verifysigapi.PvzdVerifySig')
    verifier = PvzdVerfiySig(
        '/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml',  # TODO: relative path to project root
        '/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties',
        filename_abs)
    response = verifier.verify()
    assert 'OK' == response.pvzdCode, \
        "Signature verification failed, code=" + response.pvzdCode + "; " + response.pvzdMessage
    return response.signerCertificateEncoded


def getAllowedDomains(signerCert, policyDict) -> list:
    assert policyDict["userprivilege"].get(signerCert, None) != None, 'Signer certificate not found in policy directory'
    org_id = policyDict["userprivilege"][signerCert][0]
    allowedDomains = []
    for dn in pd["domain"].keys():
        if pd["domain"][dn][0] == org_id:
            allowedDomains.append(dn)
    return allowedDomains


def validateDomainName(filename_abs, allowedDomains):
    print('allowed domains: ' + ', '.join(allowedDomains))
    pass  # TODO implement rest


def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    policyDict = getPolicyDict(invocation)
    gitHandler = GitHandler(invocation.args.pubrequ, invocation.args.verbose)
    for filename in gitHandler.getRequestQueueItems():
        filename_abs = invocation.args.pubrequ + '/' + filename
        filename_base = os.path.basename(filename)
        try:
            if invocation.args.verbose: print('\n== processing ' + filename_base + '\nvalidating XML schema')
            # validateXSD(filename_abs)
            # validateSchematron(filename_abs)
            if invocation.args.verbose: print('validating signature')
            signerCert = validateSignature(filename_abs)
            if invocation.args.verbose: print('validating signer cert')
            getAllowedDomains(signerCert, policyDict)
            if invocation.args.verbose: print('validating signer\'s privileges to use domain names')
            validateDomainName(filename_abs, policyDict)
            gitHandler.move_to_accepted(filename)
        except AssertionError as e:
            if invocation.args.verbose: print(str(e))
            gitHandler.move_to_rejected(filename)
            gitHandler.add_reject_message(filename_base, str(e))


if __name__ == '__main__':
    run_me()
