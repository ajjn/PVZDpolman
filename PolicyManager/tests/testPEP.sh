#!/bin/bash

source ./setTestEnv.sh
#echo $CLASSPATH

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

$py3 $MOD_HOME/tests/testPEP.py
