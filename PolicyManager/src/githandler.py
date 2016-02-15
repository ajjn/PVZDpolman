import logging, os, shutil
import git
from constants import *
from userexceptions import *
__author__ = 'r2h2'

class GitHandler:
    def __init__(self, repo_dir, pepout_dir, init=False, verbose=False):
        for p in (GIT_REQUESTQUEUE, GIT_DELETED, GIT_REJECTED, GIT_POLICYDIR, GIT_PUBLISHED):
            os.makedirs(os.path.join(repo_dir, p), exist_ok=True)
        os.makedirs(pepout_dir, exist_ok=True)
        if init:
            self.repo = git.Repo.init(repo_dir)
        else:
            self.repo = git.Repo(repo_dir)
        self.gitcmd = git.Git(repo_dir)
        self.repo_dir_abs = os.path.abspath(repo_dir)
        self.pepout_dir = pepout_dir
        self.rejectedpath = os.path.join(self.repo_dir_abs, GIT_REJECTED)
        self.requestedpath = os.path.join(self.repo_dir_abs, GIT_REQUESTQUEUE)
        self.deletedpath = os.path.join(self.repo_dir_abs, GIT_DELETED)
        self.verbose = verbose

    def getRequestQueueItems(self) -> str:
        """ :return: list of file names in the git repository given in pubreq  """
        return self.gitcmd.ls_files(GIT_REQUESTQUEUE).split('\n')

    def move_to_deleted(self, file):
        logging.debug('deleting file from accept directory ')
        file_to_delete = os.path.join(self.pepout_dir, file)
        if not os.path.exists(file_to_delete):
            raise ValidationError('rejected deletion request for non existing EntityDescriptor: '+ file)
        shutil.move(file_to_delete, self.deletedpath)
        self.repo.index.add([os.path.join(self.deletedpath, os.path.basename(file))])
        self.repo.index.commit('deleted')

    def move_to_accepted(self, file, sigdata):
        """ the accepted directory must be outside git to prevent any manipulation from outside """
        logging.debug('moving to accept path')
        with open(os.path.join(self.pepout_dir, os.path.basename(file)), 'w') as fd:
            fd.write(sigdata)
        file_abs = os.path.abspath(file)
        self.repo.index.remove([file_abs])
        os.remove(file_abs)
        self.repo.index.commit('accepted')

    def move_to_rejected(self, file):
        logging.debug('moving to reject directory ')
        self.repo.index.move([file, self.rejectedpath])

    def add_reject_message(self, filename_base, errortext):
        errfilename = os.path.join(self.rejectedpath, filename_base + '.err')
        with open(errfilename, 'w') as errorfile:
            errorfile.write(errortext)
        self.repo.index.add([errfilename])
        self.repo.index.commit('rejected')

    def reset_repo_with_defined_testdata(self, testdata, repo_dir):
        """  create a new repo with test data (used for unit testing) """
        repo_dir_abs = os.path.abspath(repo_dir)
        shutil.rmtree(repo_dir)
        shutil.copytree(testdata, repo_dir)
        repo = git.Repo.init(repo_dir)
        repo.index.add([os.path.join(repo_dir_abs, '*')])
        repo.index.commit('initial testdata loaded')

    def add_request_message(self, filename):
        """ used for unit tests """
        base_fn = os.path.basename(filename)
        target_fn = os.path.join(self.repo_dir_abs, GIT_REQUESTQUEUE, base_fn)
        shutil.copyfile(filename, target_fn)
        self.repo.index.add([target_fn])
        self.repo.index.commit('add requested')
