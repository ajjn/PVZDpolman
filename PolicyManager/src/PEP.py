import git
from jnius import autoclass
from invocation import *
from aodsListHandler import *
from aodsFileHandler import *

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


def getSAMLEntityDescriptors(pubreq) -> str:
    '''
    :param pubreq: path of git repo containing publication requests
    :return: list of file names in the git repository given in pubreq
    '''
    repo = git.Git(pubreq)
    return repo.ls_files('request_queue').split('\n')


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

def move_to_rejected(file):
    print('rejected ' + file)
    pass  # TODO implement


def move_to_accepted(file):
    print('accepted ' + file)
    pass  # TODO implement


def run_me(testrunnerInvocation=None):
    if testrunnerInvocation:
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    policyDict = getPolicyDict(invocation)
    for filename in getSAMLEntityDescriptors(invocation.args.pubrequ):
        filename_abs = invocation.args.pubrequ + '/' + filename
        try:
            # validateXSD(filename_abs)
            # validateSchematron(filename_abs)
            signerCert = validateSignature(filename_abs)
            getAllowedDomains(signerCert, policyDict)
            validateDomainName(filename_abs, signerCert, policyDict)
        except AssertionError as e:
            move_to_rejected(filename)
        move_to_accepted(filename)


if __name__ == '__main__':
    run_me()
