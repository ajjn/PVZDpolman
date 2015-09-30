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
