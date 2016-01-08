#!/bin/bash

source ./setEnv.sh

export aodsfile=$PROJ_HOME/PolicyManager/tests/work/aods_01_pretty.json
export repo_dir=$PROJ_HOME/PolicyManager/tests/work/policyDirectory
export trustedcerts=$PROJ_HOME/PolicyManager/tests/testdata/trustedcerts.json

~/.virtualenvs/pvzd34/bin/python \
    $PROJ_HOME/PolicyManager/src/PEP.py --verbose \
    --aods $aodsfile \
    --pubreq $repo_dir \
    --trustedcerts $trustedcerts