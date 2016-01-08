#!/bin/bash

source ./setEnv.sh

~/.virtualenvs/pvzd34/bin/python \
    $PROJ_HOME/PolicyManager/src/PEP.py --verbose \
    --aods $aodsfile \
    --pubreq $repo_dir \
    --trustedcerts $trustedcerts