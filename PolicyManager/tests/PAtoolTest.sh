#!/bin/bash

source ./setProjEnv.sh
MOD_HOME=$PROJ_HOME/PolicyManager

echo '== Test 01: create EntitDescriptor from certificate'
certificate_file="$MOD_HOME/tests/testdata/redmineIdentineticsCom-cer.pem"
entitydescriptor_file="$MOD_HOME/tests/work/redmineIdentineticsOrg_ed.xml"
md_signingcerts_file="$MOD_HOME/tests//testdata/metadatasigningcerts.json"

$py34 $MOD_HOME/src/PAtool.py -v \
    -m $md_signingcerts_file \
    -r IDP \
    createED \
    $certificate_file \
    $entitydescriptor_file


echo '== Test 02: sign EntityDescriptor'
$py34 $MOD_HOME/src/PAtool.py -v \
    -m $md_signingcerts_file \
    signED \
    $entitydescriptor_file


