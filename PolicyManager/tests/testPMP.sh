#!/bin/bash

source ./setTestEnv.sh
#echo $CLASSPATH

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

export POLMAN_TRUSTEDCERTS='/Users/admin/devl/pycharm/rhoerbe/PVZDpolman/PolicyManager/tests/testdata/trustedcerts.json'
$py3 $MOD_HOME/tests/testPMP_NoSig.py
$py3 $MOD_HOME/tests/testPMP_WithSig.py
