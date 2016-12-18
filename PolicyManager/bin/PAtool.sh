#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh

echo $PVZDPOLMAN_VERSION

args=$@
$py3 $PROJ_HOME/PolicyManager/src/PAtool.py ${args:='--help'}

