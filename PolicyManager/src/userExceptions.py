__author__ = 'r2h2'

class JSONdecodeError(Exception):
    pass


class HashChainError(Exception):
    pass



class InputFormatOrValueError(Exception):
    pass


class InputValueError(InputFormatOrValueError):
    pass


class InputFormatError(InputFormatOrValueError):
    pass


class SecurityLayerUnavailable(Exception):
    """ Security Layer (MOCCA etc.) is inactive (local port 3495 not open) """
    pass


class InvalidArgumentValue(Exception):
    pass


class EntityRoleNotSupported(Exception):
    """ Only IDP and SP roles are implemented """
    pass


class InvalidSamlXmlSchema(Exception):
    """ Invalid XML schmea for SAML metadata """
    pass