from __future__ import print_function
from contentRecord import ContentRecord
from userExceptions import *
__author__ = 'r2h2'


class InputRecord:
    ''' Handle a record to be appended '''

    def __init__(self, appendData):
        assert isinstance(appendData, dict), 'input record to be appended must be of type dict'
        assert 'record' in appendData, 'input record dict must have the key "record"'
        self.rec = ContentRecord(appendData['record'])
        self.deleteflag = appendData['delete']
        assert isinstance(self.deleteflag, bool)

    def validate(self, dir):
        try:
            self.rec.validateRec(dir, self.deleteflag)
        except (InputValueError, InputFormatError) as e:
            print('Validation failed in record with pk=' + getattr(self, 'primarykey', '<empty>'))
            raise e

