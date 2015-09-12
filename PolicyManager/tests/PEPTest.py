import os, sys
import unittest
from invocation import CliPepInvocation
import PEP
from gitHandler import GitHandler
__author__ = 'r2h2'

cwd = os.path.dirname(os.path.realpath(__file__))


class Test01_basic_happy_cycle(unittest.TestCase):
    def runTest(self):
        repo_dir = 'work/policyDirectory'
        cliClient = CliPepInvocation(['--verbose',
                                      '--aods', os.path.abspath('testdata/aods_peptest.json'),
                                      '--pubreq', os.path.abspath(repo_dir),
                                      '--trustedcerts', os.path.abspath('testdata/trustedcerts.json')])
        print('= creating fresh git repo in ' + repo_dir)
        gitHandler = GitHandler(cliClient.args.pubrequ, cliClient.args.verbose)
        gitHandler.reset_repo('testdata/policyDirectory', repo_dir)
        print('= processing request queue')
        PEP.run_me(cliClient)



if __name__ == '__main__':
    unittest.main()
