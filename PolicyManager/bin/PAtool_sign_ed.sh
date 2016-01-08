#!/bin/bash

source ./setEnv.sh

export in_entitydescriptor_file=$1
export md_signingcerts_file="$PROJ_HOME/PolicyManager/tests/testdata/metadatasigningcerts.json"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 entitydescriptor_file_to_be_signed"
fi

$py3 $PROJ_HOME/PolicyManager/src/PAtool.py -v \
    -m $md_signingcerts_file \
    signED \
    $in_entitydescriptor_file

