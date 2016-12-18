#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh
source $SCRIPTDIR/setConfig.sh

echo $PVZDPOLMAN_VERSION

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    $py3 $PROJ_HOME/PolicyManager/src/PEP.py $1 $2
    exit 0
fi

if [ "$1" == "-d" ] || [ "$1" == "--debug" ]; then
    export PEPLOGLEVEL=DEBUG
fi

$py3 $PROJ_HOME/PolicyManager/src/PEP.py --list_trustedcerts --loglevel=$PEPLOGLEVEL