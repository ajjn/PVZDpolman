#!/bin/bash

source ./setTestEnv.sh
echo $CLASSPATH

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

$py3 $UTRUNNER $MOD_HOME/tests/PMPTestNoSig.py true
