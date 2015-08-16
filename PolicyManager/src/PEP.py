
import git
from invocation import *
from aodsListHandler import *
from aodsFileHandler import *
__author__ = 'r2h2'

''' Policy Management Point does this operation each invocation:
    browse a well-known git location for XML files
    for each file:
        check if it conforms to the policy
        if it is OK, move it to the 'accepted' directory
        else move it to the 'rejected' directory

    Policy check includes these policies:
        valid SAML entity descriptor (XSD conformance)
        valid SAML entity descriptor (profile XSLT conformance)
        valid signature
        signing certificate in the policy
'''

def getPolicyList(invocation):
    aodsHandlder = AODSFileHandler(invocation)
    aodsList = AodsList(invocation.args.verbose);
    return aodsList.aods_read(aodsHandlder)

def getSAMLEntityDescriptors(pubreq):
    '''
    :param pubreq: path of git repo containing publication requests
    :return: list of file names in the git repository given in pubreq
    '''
    repo = git.Git(pubreq)
    return repo.ls_files().split('\n')

def validateXSD(file):
    XmlValidator = autoclass('at.wien.ma14.pvzd.validateXSD');
    validator = XmlValidator('ValidateXSD/SAML_MD_Schema')
    validator.validateXmlAgainstXsds(file)


def run_me(testrunnerInvocation=None):
    if (testrunnerInvocation):
        invocation = testrunnerInvocation
    else:
        invocation = CliPepInvocation()

    policyDict = getPolicyList(invocation)
    for file in getSAMLEntityDescriptors(invocation.args.pubrequ):
        pass

if __name__ == '__main__':
    run_me()
