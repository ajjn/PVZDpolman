import argparse, getpass, sys
__author__ = 'r2h2'


class AbstractInvocation():
    ''' Allow invocations from CLI/test runner, GUI '''
    pass


class CliPmpInvocation(AbstractInvocation):
    ''' define CLI invocation for PMP. Test runner can use this by passing testargs '''
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Management Point')
        self._parser.add_argument('-a', '--aods', dest='aods', default='aods.json', help='Journal file (Policy Directory)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true", help='trace hash chain computation')
        self._parser.add_argument('-r', '--registrant', dest='registrant', default='',
                                  help='Person adding the input record (current user)')
        self._parser.add_argument('-s', '--submitter', dest='submitter', default=getpass.getuser(),
                                  help='Person that submitted the input record')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts', default='trustedcerts.json',
                                  help='file containing json-array of PEM-formatted certificates trusted to sign the aods')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-x', '--xmlsign', action="store_true", help='sign using citizen card)')
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the parser for the "create" command
        self._parser_create = _subparsers.add_parser('create', help='create a new journal')

        # create the parser for the "append" command
        self._parser_append = _subparsers.add_parser('append', help='append a record to the journal')
        self._parser_append.add_argument('input', type=argparse.FileType('r'),
                                         help='file containing the records to be added in JSON')

        # create the parser for the "read" command
        self._parser_append = _subparsers.add_parser('read', help='read, verify and transform the journal')
        self._parser_append.add_argument('-j', '--jsondump', action="store_true", help='dump policy dict as JSON)')
        self._parser_append.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None,
                                         help='dump policy dictionary file)')
        #self._parser_append.add_argument('-r', '--range', choices=['all', 'from', 'new'], default='all',
        #                                 help='read all (starting with the big bang), or new (what has changes since last time)')
        #self._parser_append.add_argument('-s', '--sequence', type=int, help='output from this record onwards')

        if (testargs):
            self._parser_append = _subparsers.add_parser('scratch', help='scratch the AODS')
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if not self.args.verbose:
            sys.tracebacklimit = 2


class CliPepInvocation(AbstractInvocation):
    ''' define CLI invocation for PEP.  Test runner can use this by passing testargs '''
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Enforcement Point')
        self._parser.add_argument('-a', '--aods', dest='aods', default='aods.json', help='AODS file (Policy Directory)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true", help='trace hash chain computation')
        self._parser.add_argument('-r', '--pubrequ', dest='pubrequ', default='.',
                                  help='root path of git repo containing the publication request')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts', default='trustedcerts.json',
                                  help='file containing json-array of PEM-formatted certificates trusted to sign the aods')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-x', '--xmlsign', action="store_true", help='use signed aods policy directory)')

        if (testargs):
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if not self.args.verbose:
            sys.tracebacklimit = 2


class CliPAtoolInvocation(AbstractInvocation):
    ''' define CLI invocation for PAtool. Test runner can use this by passing testargs  '''
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Portaladministrator Tool')
        self._parser.add_argument('-m', '--metadatacerts', dest='metadatacerts', default='metadatacerts.json',
                                  help='file containing json-array of PEM-formatted certificates trusted to sign the metadata aggregate')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-s', '--signed_output', dest='signed_output',
                                  help='signED output file (default: s/(inputfile).xml/\1_signed.xml/)')
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the parser for the "createED" command
        self._parser_create = _subparsers.add_parser('createED', help='create an EntityDescriptor from a certificate')
        self._parser_create.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None, help='output file)')

        # create the parser for the "signED" command
        self._parser_sign = _subparsers.add_parser('signED', help='sign an EntityDescriptor using the Citizen Card')
        self._parser_sign.add_argument('input', type=argparse.FileType('r'),help='file containing the EntityDescriptor')

        # create the parser for the "extractED" command
        self._parser_extract = _subparsers.add_parser('extractED', help='extract certificate from EntityDescriptors in metadata')
        self._parser_extract.add_argument('input', type=argparse.FileType('r'), help='file containing the metadata aggregate')

        if (testargs):
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if not self.args.verbose:
            sys.tracebacklimit = 2
