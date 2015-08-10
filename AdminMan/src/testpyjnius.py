__author__ = 'admin'

from jnius import autoclass
// OSX: pyjnius requires dyblib setting, e.g.:
// export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$(/usr/libexec/java_home)/jre/lib/server

PvzdVerfiySig = autoclass('at.wien.ma14.pvzd.PvzdVerfiySig');
PvzdVerifySigResponse = autoclass('at.wien.ma14.pvzd.PvzdVerifySigResponse');
verifier = PvzdVerfiySig(
    "/opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xml",
    "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf/log4j.properties",
    "/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata/idp5_valid.xml_sig.xml")

response  = verifier.verify();
print(response.pvzdCode)

