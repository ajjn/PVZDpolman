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


class EmptySamlED(Exception):
    """ SAML metadata file is empty or does not exist """
    pass


class EmptyAODS(Exception):
    """ Policy Journal file is empty and will not be saved"""
    pass


class InvalidSamlXmlSchema(Exception):
    """ Invalid XML schmea for SAML metadata """
    pass


class ValidationFailure(Exception):
    """ application-level validation failure """
    pass


class EntityRoleNotSupported(ValidationFailure):
    """ Only IDP and SP roles are implemented """
    pass


class CertExpired(ValidationFailure):
    """ certificate has a notValidAfter date in the pas """
    pass


class CertInvalid(ValidationFailure):
    """ certificate was not issued by a accredited CA """
    pass


class InvalidFQDN(ValidationFailure):
    """ The FQDN is not in the allowed domains """
    pass


class MissingRootElem(ValidationFailure):
    """ Expected XML root element not found """
    pass


class UnauthorizedSigner(ValidationFailure):
    """ Signer certificate not found not found in policy directory """
    pass


class SignatureVerificationFailed(ValidationFailure):
    """ Signature verification failed """
    pass


class PMPInputRecNoDict(ValidationFailure):
    """ PMP input record is not a non-empty list of dict """
    pass

class MissingArgument(ValidationFailure):
    """ required argument missing """
    pass

