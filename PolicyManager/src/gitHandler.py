import os, shutil
import git
from constants import *
__author__ = 'r2h2'

class GitHandler:
    def __init__(self, repo_dir, verbose):
        self.repo = git.Repo(repo_dir)
        self.gitcmd = git.Git(repo_dir)
        repo_dir_abs = os.path.abspath(repo_dir)
        self.acceptpath = os.path.join(repo_dir_abs, GIT_ACCEPTED)
        self.rejectpath = os.path.join(repo_dir_abs, GIT_REJECTED)
        self.verbose = verbose

    def getRequestQueueItems(self) -> str:
        ''' :return: list of file names in the git repository given in pubreq  '''
        return self.gitcmd.ls_files(GIT_REQUESTQUEUE).split('\n')

    def remove_from_accepted(self, file):
        if self.verbose: print('removing file from request_queue and accept directory ')
        self.repo.index.move([file, self.acceptpath]) # TODO implement
        self.repo.index.commit('accepted')

    def move_to_accepted(self, file):
        if self.verbose: print('moving to accept directory ')
        self.repo.index.move([file, self.acceptpath])
        self.repo.index.commit('accepted')

    def move_to_rejected(self, file):
        if self.verbose: print('moving to reject directory ')
        self.repo.index.move([file, self.rejectpath])

    def add_reject_message(self, filename_base, errortext):
        errfilename = os.path.join(self.rejectpath, filename_base + '.err')
        with open(errfilename, 'w') as errorfile:
            errorfile.write(errortext)
        self.repo.index.add([errfilename])
        self.repo.index.commit('accepted')

    def reset_repo_with_defined_testdata(self, testdata, repo_dir):
        '''  create a new repo with test data (used for unit testing) '''
        repo_dir_abs = os.path.abspath(repo_dir)
        shutil.rmtree(repo_dir)
        shutil.copytree(testdata, repo_dir)
        repo = git.Repo.init(repo_dir)
        repo.index.add([os.path.join(repo_dir_abs, '*')])
        repo.index.commit('initial testdata loaded')
