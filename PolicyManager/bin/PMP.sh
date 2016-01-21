#!/bin/bash

source ./setEnv.sh
source ./setConfig.sh

$py3 $PROJ_HOME/PolicyManager/src/PMP.py -x -a $POLICY_JOURNAL -t $TRUSTEDCERTS $@
