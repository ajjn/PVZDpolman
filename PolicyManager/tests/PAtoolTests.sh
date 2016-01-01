#!/bin/bash

source ./setTestEnv.sh
echo "CLASSPATH=$CLASSPATH"
echo
MOD_HOME=$PROJ_HOME/PolicyManager

echo '== Test 01: create EntitDescriptor from certificate'
certificate_file="$MOD_HOME/tests/testdata/gondorMagwienGvAt_2017-cer.pem"
entitydescriptor_file="$MOD_HOME/tests/work/gondorMagwienGvAt_ed.xml"
md_signingcerts_file="$MOD_HOME/tests/testdata/metadatasigningcerts.json"

$py3 $MOD_HOME/src/PAtool.py -v \
    --metadatacerts $md_signingcerts_file \
    --entityid https://gondor.magwien.gv.at/idp \
    --samlrole IDP \
    createED \
    $certificate_file \
    $entitydescriptor_file


echo '== Test 02: sign EntityDescriptor'
$py3 $MOD_HOME/src/PAtool.py -v \
    -m $md_signingcerts_file \
    signED \
    $entitydescriptor_file


echo '== Test 03: sign EntityDescriptor with invalid SAML schema'
$py3 $MOD_HOME/src/PAtool.py -v \
    -m $md_signingcerts_file \
    signED \
    "$MOD_HOME/tests/testdata/PEP02_gondorMagwienGvAt_ed_invalid_xsd.xml"

