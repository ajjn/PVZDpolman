import difflib, logging, os.path
__author__ = 'r2h2'

def assertNoDiff(testresult_filename, subdir=None):
    ''' compare argument file in work/ with file with same name but in testdata/
    :param testresult_filename: namepart onyl, no path
    :return: assert message
    '''
    if subdir is None:
        f_testdata = open(os.path.abspath(os.path.join('testdata', testresult_filename)))
        f_work = open(os.path.abspath(os.path.join('work', testresult_filename)))
    else:
        f_testdata = open(os.path.abspath(os.path.join('testdata', subdir, testresult_filename)))
        f_work = open(os.path.abspath(os.path.join('work', subdir, testresult_filename)))
    diff = difflib.unified_diff(f_work.readlines(), f_testdata.readlines())
    f_work.close()
    f_testdata.close()
    try:
        assert ''.join(diff) == '', 'result (' + testresult_filename + ') is not equal to reference data'
    except AssertionError as e:
        logging.error('     result (' + testresult_filename + ')is not equal to reference data.')
        logging.debug(e)

