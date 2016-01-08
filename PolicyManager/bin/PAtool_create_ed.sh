#!/bin/bash

source setEnv.sh

export certificate_file=$1
export entitydescriptor_file=$2
export md_signingcerts_file="$PROJ_HOME/PolicyManager/tests/testdata/metadatasigningcerts.json"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 certificate_file entitydescriptor_file"
fi

$py3 $PROJ_HOME/PolicyManager/src/PAtool.py -v \
    -m $md_signingcerts_file \
    -r IDP \
    createED \
    $certificate_file \
    $entitydescriptor_file
