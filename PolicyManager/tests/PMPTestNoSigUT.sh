#!/bin/bash

source ./setTestEnv.sh

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

$py34 $UTRUNNER $MOD_HOME/tests/PMPTestNosign.py true
