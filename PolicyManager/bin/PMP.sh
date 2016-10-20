#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh
source $SCRIPTDIR/setConfig.sh

args=$@
$py3 $PROJ_HOME/PolicyManager/src/PMP.py ${args:='--help'}
