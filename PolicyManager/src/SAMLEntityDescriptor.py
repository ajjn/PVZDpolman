import os
from jnius import autoclass

__author__ = 'r2h2'


class SAMLEntityDescriptor:
    def __init__(self, filename_abs, projdir_abs):
        self.filename_abs = filename_abs
        self.projdir_abs = projdir_abs

    def validateXSD(self):
        xsdValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XSDValidator')
        validator = xsdValidator(os.path.join(self.projdir_abs, 'lib/SAML_MD_Schema'), False)
        return validator.validateSchema(self.filename_abs)


