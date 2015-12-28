from gitHandler import GitHandler
import os

repo_dir = 'work/policyDirectory'
gitHandler = GitHandler(os.path.abspath(repo_dir), True)
gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory', repo_dir)
gitHandler.move_to_accepted('request_queue/02_idp5_valid_sig_untrusted_signer.xml')
