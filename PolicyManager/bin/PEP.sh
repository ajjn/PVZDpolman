#!/bin/bash

source ./setEnv.sh

$py3    $PROJ_HOME/PolicyManager/src/PEP.py --verbose \
    --aods $aodsfile \
    --pubreq $repo_dir \
    --trustedcerts $trustedcerts