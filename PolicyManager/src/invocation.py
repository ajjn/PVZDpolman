import argparse, getpass, sys
from constants import LOGLEVELS
from userexceptions import ValidationError

__author__ = 'r2h2'


class AbstractInvocation():
    """ Allow invocations from CLI/test runner, GUI """
    pass


class CliPmpInvocation(AbstractInvocation):
    """ define CLI invocation for PMP. Test runner can use this by passing testargs """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Management Point')
        self._parser.add_argument('-a', '--aods', dest='aods', required=True,
                                  help='Policy journal (append only data strcuture)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true",
                                  help='trace hash chain computation')
        self._parser.add_argument('-r', '--registrant', dest='registrant', default='',
                                  help='Person adding the input record (current user)')
        self._parser.add_argument('-s', '--submitter', dest='submitter', default=getpass.getuser(),
                                  help='Person that submitted the input record')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts', default='trustedcerts.json',
                                  help='file containing json-array of PEM-formatted certificates trusted to sign the aods')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-x', '--xmlsign', action="store_true",
                                  help='store policy journal as signed XML')
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the parser for the "create" command
        self._parser_create = _subparsers.add_parser('create', help='create a new journal')

        # create the parser for the "append" command
        self._parser_append = _subparsers.add_parser('append', help='append a record to the journal')
        self._parser_append.add_argument('input', type=argparse.FileType('r'),
                                         help='file containing the records to be added in JSON')

        # create the parser for the "read" command
        self._parser_append = _subparsers.add_parser('read', help='read, verify and transform the journal')
        self._parser_append.add_argument('-P', '--poldirhtml', action="store_true",
                                         help='output policy directory as HTML)')
        self._parser_append.add_argument('-p', '--poldirjson', action="store_true",
                                         help='dump policy directory as JSON)')
        self._parser_append.add_argument('-j', '--journal', action="store_true",
                                         help='output Journal as JSON)')
        self._parser_append.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None,
                                         help='dump policy directory file)')
        # TODO: implement range and diff listings
        #self._parser_append.add_argument('-r', '--range', choices=['all', 'from', 'new'], default='all',
        #                                 help='read all (starting with the big bang), or new (what has changes since last time)')
        #self._parser_append.add_argument('-s', '--sequence', type=int, help='output from this record onwards')

        # create the parser for the "revokeCert" command
        self._parser_revoke = _subparsers.add_parser('revokeCert', help='revoke certificate')
        self._parser_revoke.add_argument('cert', type=argparse.FileType('r'), nargs='?', default=None,
                                         help='certificate to be revoked')


        if (testargs):
            self._parser_append = _subparsers.add_parser('scratch', help='scratch the AODS')
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv
        self.args.list_trustedcerts = False  # only used in PEP
        if self.args.subcommand == 'read':
            if sum(bool(x) for x in (getattr(self.args, 'poldirhtml', False),
                                     getattr(self.args, 'poldirjson', False),
                                     getattr(self.args, 'journal', False))) > 1:
                raise ValidationError("-j/--journal, -P/--poldirhtml and -p/--poldirjson are mutually exclusive")


class CliPepInvocation(AbstractInvocation):
    """ define CLI invocation for PEP.  Test runner can use this by passing testargs """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Enforcement Point')
        self._parser.add_argument('-a', '--aods', dest='aods', required=True,
                                  help='Policy journal (AODS = append only data strcuture)')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true",
                                  help='trace hash chain computation')
        self._parser.add_argument('-l', '--list_trustedcerts', action="store_true",
                                  help='list trusted vertificates on startup (needs level=DEBUG)')
        self._parser.add_argument('-L', '--loglevel', dest='loglevel_str', choices=LOGLEVELS.keys(),
                                  help='Level for file logging')
        self._parser.add_argument('-r', '--pubrequ', dest='pubrequ', default='.',
                                  help='root path of git repo containing the publication request')
        self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts', default='trustedcerts.json',
                                  help='file containing json-array of PEM-formatted certificates trusted to sign the policy journal')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        self._parser.add_argument('-x', '--xmlsign', action="store_true",
                                  help='use signed xml format for policy journal)')

        if (testargs):
            self.args = self._parser.parse_args(testargs)
            self.args.unittest = True  # used to filter log events depending on prod vs. test
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv
            self.args.unittest = False

        if not hasattr(self.args, 'loglevel_str') or self.args.loglevel_str is None:
            self.args.loglevel_str = 'INFO'
        self.args.loglevel = LOGLEVELS[self.args.loglevel_str]


class CliPAtoolInvocation(AbstractInvocation):
    """ define CLI invocation for PAtool. Test runner can use this by passing testargs  """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Portaladministrator Tool')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the parser for the "createED" command
        self._parser_create = _subparsers.add_parser('createED', help='create an EntityDescriptor from a certificate')
        self._parser_create.add_argument('-e', '--entityid', dest='entityid',
                                         help="overwrite default entityId generated from the certificate's subject-CN and role type")
        self._parser_create.add_argument('-S', '--entityidSuffix', dest='entityid_suffix', default='',
                                         help="used to distinguish multiple entities with a single FQDN")
        self._parser_create.add_argument('-r', '--samlrole', dest='samlrole', required=True, choices=('IDP', 'SP'))
        self._parser_create.add_argument('cert', type=argparse.FileType('r'), nargs='?', default='', help='certificate)')
        self._parser_create.add_argument('output', type=argparse.FileType('w'), nargs='?', default='', help='output file)')

        # create the parser for the "signED" command
        self._parser_sign = _subparsers.add_parser('signED', help='sign an EntityDescriptor using the Citizen Card')
        self._parser_sign.add_argument('-s', '--signed_output', dest='signed_output',
                                       help='signED output file (default: s/(inputfile).xml/\1_signed.xml/)')
        self._parser_sign.add_argument('input', type=argparse.FileType('r'),help='file containing the EntityDescriptor')

        # create the parser for the "extractED" command
        self._parser_extract = _subparsers.add_parser('extractED', help='extract certificate from EntityDescriptors in metadata')
        self._parser_extract.add_argument('input', type=argparse.FileType('r'), help='file containing the metadata aggregate')

        # create the parser for the "deleteED" command
        self._parser_delete = _subparsers.add_parser('deleteED', help='create a request to delete an entityDescriptor')
        self._parser_delete.add_argument('-e', '--entityid', dest='entityid',
                                         help="overwrite default entityId generated from the certificate's subject-CN and role type")
        self._parser_delete.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None, help='output file)')

        # create the parser for the "revokeCert" command
        self._parser_revoke = _subparsers.add_parser('revokeCert', help='create a PMP input file to revoke a certificate')
        self._parser_revoke.add_argument('-c', '--certfile', dest='certfile', type=argparse.FileType('r'))
        self._parser_revoke.add_argument('-R', '--reason', dest='reason', help='test explaining the reason for the revocation')
        self._parser_revoke.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None, help='PMP input file)')

        # create the parser for the "caCert" command
        self._parser_revoke = _subparsers.add_parser('caCert', help='create a PMP input file to import a ca certificate')
        self._parser_revoke.add_argument('-c', '--certfile', dest='certfile', type=argparse.FileType('r'))
        self._parser_revoke.add_argument('-p', '--pvprole', dest='pvprole', choices=('IDP', 'SP'), help='IDP, SP')
        self._parser_revoke.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None, help='PMP input file)')

        # create the parser for the "adminCert" command
        self._parser_revoke = _subparsers.add_parser('adminCert', help='create a PMP input file to import an admin certificate')
        self._parser_revoke.add_argument('-o', '--orgid', dest='orgid', help='Organization ID')
        self._parser_revoke.add_argument('output', type=argparse.FileType('w'), nargs='?', default=None, help='PMP input file)')

        if testargs:
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if self.args.subcommand == 'createED':
            if self.args.entityid is not None:
                if self.args.entityid[0:8] != 'https://':
                    raise ValidationError('entityId must start with https://')
        if self.args.subcommand == 'revokeCert' and not getattr(self.args, 'reason', False):
            raise ValidationError('must specify --reason for command revokeCert')
        if self.args.subcommand == 'caCert':
            if not getattr(self.args, 'pvprole', False):
                raise ValidationError('must specify --pvprole for command caCert')
        if self.args.subcommand == 'adminCert':
            if not getattr(self.args, 'orgid', False):
                raise ValidationError('must specify --orgid for command adminCert')
            if not getattr(self.args, 'output', False):
                raise ValidationError('must specify output for command adminCert')
