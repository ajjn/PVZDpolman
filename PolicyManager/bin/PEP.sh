#!/bin/bash

source ./setEnv.sh
source ./setConfig.sh

$py3 $PROJ_HOME/PolicyManager/src/PEP.py \
    --aods $POLICY_JOURNAL -x \
    --pubreq $REPO_DIR \
    --trustedcerts $TRUSTEDCERTS \
    --list_trustedcerts \
    --loglevel=INFO