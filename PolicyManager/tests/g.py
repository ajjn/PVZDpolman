import os, shutil
import git
from gitHandler import GitHandler


GIT_REQUESTQUEUE = 'request_queue'
GIT_ACCEPTED = 'accepted'
GIT_REJECTED = 'rejected'

repo_dir = 'work/policyDirectory'
testdata = 'testdata/policyDirectory'
repo_dir_abs = os.path.abspath(repo_dir)

repo_dir = 'work/policyDirectory'
gitHandler = GitHandler(os.path.abspath(repo_dir), True)
gitHandler.reset_repo_with_defined_testdata('testdata/policyDirectory', repo_dir)


acceptpath = os.path.join(repo_dir_abs, GIT_ACCEPTED)
rejectpath_abs = os.path.join(repo_dir_abs, GIT_REJECTED)
rejectpath_rel = os.path.join(repo_dir, GIT_REJECTED)

file = os.path.join(repo_dir_abs, GIT_REQUESTQUEUE, '02_idp5_valid_sig_untrusted_signer.xml')
print('file=%s, rejectpath=%s' %(file, rejectpath_abs))
repo = git.Repo(repo_dir)
repo.index.move([file, rejectpath_abs])
repo.index.commit(file + ' rejected')
filename_base = os.path.basename(file)
errfilename = os.path.join(rejectpath_rel, filename_base + '.err')
print(errfilename)
with open(errfilename, 'w') as errorfile:
    errorfile.write('blah')

repo.index.add(errfilename)
repo.index.commit('rejectpath')
