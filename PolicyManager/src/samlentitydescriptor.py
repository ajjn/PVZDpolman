# STUB version of PATool for simlified development

import logging, os, re, sys
#from constants import PROJDIR_ABS

__author__ = 'r2h2'


class SAMLEntityDescriptor:
    def __init__(self,
                 ed_file_handle=None,
                 createfromcertstr=None, entityid=None, samlrole=None,
                 delete_entityid=None):
        """ Create a SAMLEntityDescriptor with either of 3 methods:
                1. from a xml file with an EntityDescriptor as root element, or
                2. from a certificate + a saml role, or
                3. from an entityID as a delete request
        """
        if sum(x is not None for x in (ed_file_handle, createfromcertstr, delete_entityid)) != 1:
            raise InputValueError('only one argument out of (ed_file_handle, createfromcertstr, delete_entityid) allowed')
        if ed_file_handle is not None:   # case 1
            self.ed_file_handle = ed_file_handle
            self.ed_filename_abs = os.path.abspath(ed_file_handle.name)
            if not os.path.isfile(self.ed_filename_abs) or os.path.getsize(self.ed_filename_abs) == 0:
                raise EmptySamlEDError(self.ed_filename_abs + ' empty or missing')
            assert self.ed_filename_abs[-4:] == '.xml', 'input file must have the extension .xml'
            with open(self.ed_filename_abs) as f:
                self.xml_str = f.read()
        elif delete_entityid is not None:
            self.xml_str = self.create_delete(delete_entityid)
        else:
            self.xml_str = self.cert2entitydescriptor(createfromcertstr, entityid, samlrole)
        #self.dom = ET.fromstring(self.xml_str.encode('utf-8'))
        #if self.dom.tag != '{urn:oasis:names:tc:SAML:2.0:metadata}EntityDescriptor':
        #    raise InputValueError('XML file must have md:EntityDescriptor as root element')


    def get_entityid(self):
        return 'https://dummy.entityid.test/xx'


    def get_xml_str(self):
        return self.xml_str


    def get_filename(self) -> str:
        """ remove non-alpha characters, uppercase first char after no-alpha;
            add _ after hostname and .xml as extension
        """
        x = re.sub(r'^https?://', '', self.get_entityid())
        r = ''
        upper = False
        in_path = False
        for i in range(0, len(x)):
            if x[i].isalpha() or x[i].isdigit():
                if upper:
                    r += x[i].upper()
                else:
                    r += x[i]
                upper = False
            elif not in_path and x[i] == '/':
                r += '_'
                in_path = True
            else:
                upper = True
        return r + '.xml'


    def cert2entitydescriptor(self, cert_str, entityid, samlrole):
        if samlrole == 'IDP':
            entityDescriptor = """\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:pvzd="http://egov.gv.at/pvzd1.xsd">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>""".format(eid=entityid, pem=cert_str)
        elif samlrole == 'SP':
            entityDescriptor = """\
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:pvzd="http://egov.gv.at/pvzd1.xsd">
  <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo>
        <ds:X509Data>
           <ds:X509Certificate>
{pem}
           </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
      <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/acs/unused" index="0" isDefault="true"/>
    </md:KeyDescriptor>
  </md:SPSSODescriptor>
</md:EntityDescriptor>""".format(eid=entityid, pem=cert_str)
        return entityDescriptor

    def create_delete(self, entityid):
        entityDescriptor = """\
<!-- DELETE entity descriptor from metadata -->
<md:EntityDescriptor entityID="{eid}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:pvzd="http://egov.gv.at/pvzd1.xsd"
    pvzd:disposition="delete">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{eid}/idp/unused"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>""".format(eid=entityid)
        return entityDescriptor
