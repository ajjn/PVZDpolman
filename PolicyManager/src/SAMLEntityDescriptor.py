import os
from jnius import autoclass

__author__ = 'r2h2'

class SAMLEntityDescriptor:
    def __init__(self, filename_abs, projdir_abs):
        self.filename_abs = filename_abs
        self.projdir_abs = projdir_abs

    def validateXSD(self):
        XmlValidator = autoclass('at.wien.ma14.pvzd.validatexsd.XmlValidator')
        validator = XmlValidator(os.path.join(self.projdir_abs, 'ValidateXSD/SAML_MD_Schema'), False)
        validator.validateSchema(self.filename_abs)

