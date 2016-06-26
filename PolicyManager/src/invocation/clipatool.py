import argparse, getpass, sys
import urllib.parse
from . import AbstractInvocation
from userexceptions import *

__author__ = 'r2h2'


class CliPatool(AbstractInvocation):
    """ define CLI invocation for PAtool. Test runner can use this by passing testargs  """
    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Portaladministrator Tool')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the parser for the "createED" command
        self._parser_create = _subparsers.add_parser('createED',
            help='create (and optionally sign) a minimal EntityDescriptor from a certificate. Filename is derived from entityId')
        self._parser_create.add_argument('-e', '--entityid', dest='entityid',
            help="overwrite default entityId generated from the certificate's subject-CN and role type")
        self._parser_create.add_argument('-o', '--outputdir', dest='output_dir', required=True,
            help='directory of signed output file. Filename is derived from entityId')
        self._parser_create.add_argument('-r', '--samlrole', dest='samlrole',
                                         required=True, choices=('IDP', 'SP'))
        self._parser_create.add_argument('-s', '--sign', dest='sign', action="store_true",
             help='sign after create')
        self._parser_create.add_argument('-S', '--entityidSuffix', dest='entityid_suffix', default='',
            help="used to distinguish multiple entities with a single FQDN")
        self._parser_create.add_argument('cert', type=argparse.FileType('r'), help='certificate')

        # create the parser for the "signED" command
        self._parser_sign = _subparsers.add_parser('signED',
             help='sign an EntityDescriptor using the Citizen Card')
        self._parser_sign.add_argument('-o', '--outputdir', dest='output_dir', required=True,
            help='Directory of signED output file')
        self._parser_sign.add_argument('input', type=argparse.FileType('r'),
            help='file containing the unsigned EntityDescriptor..')

        # create the parser for the "extractED" command
        #self._parser_extract = _subparsers.add_parser('extractED',
        #    help='extract certificate from EntityDescriptors in metadata')
        #self._parser_extract.add_argument('input', type=argparse.FileType('r'),
        #    help='file containing the metadata aggregate')

        # create the parser for the "deleteED" command
        self._parser_delete = _subparsers.add_parser('deleteED',
             help='create a request to delete an entityDescriptor')
        self._parser_delete.add_argument('-e', '--entityid', dest='entityid', required=True,
            help="entityId generated from the certificate's subject-CN and role type")
        self._parser_delete.add_argument('-o', '--outputdir', dest='output_dir', required=True,
            help='directory of signed output file. Filename is derived from entityId')

        # create the parser for the "revokeCert" command
        self._parser_revoke = _subparsers.add_parser('revokeCert',
            help='create a PMP input file to revoke a certificate')
        self._parser_revoke.add_argument('-c', '--certfile', dest='certfile',
                                         type=argparse.FileType('r'), required=True)
        self._parser_revoke.add_argument('-R', '--reason', dest='reason', required=True,
            help='test explaining the reason for the revocation')
        self._parser_revoke.add_argument('output', type=argparse.FileType('w'), default=None,
            help='PMP input file')

        # create the parser for the "caCert" command
        self._parser_caCert = _subparsers.add_parser('caCert',
             help='create a PMP input file to import a ca certificate')
        self._parser_caCert.add_argument('-c', '--certfile', dest='certfile', type=argparse.FileType('r'))
        self._parser_caCert.add_argument('-p', '--pvprole', dest='pvprole', required=True,
                                         choices=('IDP', 'SP'), help='IDP, SP')
        self._parser_caCert.add_argument('output', type=argparse.FileType('w'), default=None,
            help='PMP input file)')

        # create the parser for the "adminCert" command
        self._parser_adminCert = _subparsers.add_parser('adminCert',
             help='create a PMP input file to import an admin certificate')
        self._parser_adminCert.add_argument('-o', '--orgid', dest='orgid',
                                            required=True, help='Organization ID')
        self._parser_adminCert.add_argument('output', type=argparse.FileType('w'), help='PMP input file')

        # create the parser for the "exportCerts" command
        self._parser_exportCerts = _subparsers.add_parser('exportCerts',
             help='export certificates from metadata aggregate')
        self._parser_exportCerts.add_argument('-m', '--md-cert', dest='md_cert', required=True,
            help='Certificate for metadata signature')
        self._parser_exportCerts.add_argument('-o', '--outputdir', dest='output_dir', required=True,
            help='directory to output certificates. Filenames are derived from entityId')
        self._parser_exportCerts.add_argument('-r', '--samlrole', dest='pvprole',
                                         choices=('IDP', 'SP'), help='IDP, SP')
        self._parser_exportCerts.add_argument('metadata', type=argparse.FileType('r'), help='SAML Metadata aggregate file)')

        if testargs:
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        if self.args.subcommand == 'createED':
            if self.args.entityid is not None:
                url = urllib.parse.urlparse(self.args.entityid)
                if url[0] != 'https':
                    raise ValidationError('entityId must be a URL with https schema')
        elif self.args.subcommand == 'signED':
            self.args.input_fn = self.args.input.name
            self.args.input.close()
        elif self.args.subcommand == 'exportCerts':
            # close file an pass it as name (handle open/close locally)
            fn = self.args.metadata.name
            self.args.metadata.close()
            self.args.metadata = fn
