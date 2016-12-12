#!/bin/bash

SCRIPTDIR=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
source $SCRIPTDIR/setTestEnv.sh
#echo $CLASSPATH

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

$py3 $MOD_HOME/tests/testPEP.py
