import difflib, logging, os.path
__author__ = 'r2h2'

def assertNoDiff(testresult_filename):
    ''' compare argument file in work/ with file with same name but in testdata/
    :param testresult_filename: namepart onyl, no path
    :return: assert message
    '''
    diff = difflib.unified_diff(open(os.path.abspath(os.path.join('work', testresult_filename))).readlines(),
                                open(os.path.abspath(os.path.join('testdata', testresult_filename))).readlines())
    try:
        assert ''.join(diff) == '', 'result (' + testresult_filename + ') is not equal to reference data'
    except AssertionError as e:
        logging.error('     result (' + testresult_filename + ')is not equal to reference data.')
        logging.debug(e)

