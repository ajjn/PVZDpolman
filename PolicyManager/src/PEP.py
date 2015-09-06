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

def getPolicyDict(invocation):
    aodsHandlder = AODSFileHandler(invocation)
    aods = AodsList(invocation.args.verbose)
    return aods.aods_read(aodsHandlder)

def getSAMLEntityDescriptors(pubreq):
    '''
    :param pubreq: path of git repo containing publication requests
    :return: list of file names in the git repository given in pubreq
    '''
    repo = git.Git(pubreq)
    return repo.ls_files().split('\n')

def validateXSD(file):
    XmlValidator = autoclass('at.wien.ma14.pvzd.validateXSD')
    validator = XmlValidator('ValidateXSD/SAML_MD_Schema')
    validator.validateXmlAgainstXsds(file)

def validateSignature(fileName):
    # verify xmldsig
    PvzdVerfiySig = autoclass('PvzdVerifySig')
    verifier = PvzdVerfiySig(
        '/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml', # TODO: relative path to project root
        '/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties',
        fileName)
    response = verifier.verify()
    assert 'OK' == response.pvzdCode, \
        "Signature verification failed, code=" + response.pvzdCode + "; " + response.pvzdMessage
    return response.signerCertificateEncoded

def lookupSignerCert(signerCert, policyDict):
    access = policyDict["userprivilege"] attr[0]

def run_me(testrunnerInvocation=None):
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    policyDict = getPolicyDict(invocation)
    for file in getSAMLEntityDescriptors(invocation.args.pubrequ):
        signerCert = validateSignature(file)
        lookupSignerCert(signerCert, policyDict)


if __name__ == '__main__':
    run_me()
