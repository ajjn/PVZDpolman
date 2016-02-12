#!/bin/bash

source ./setEnv.sh
source ./setConfig.sh

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    $py3 $PROJ_HOME/PolicyManager/src/PEP.py $1 $2
fi

$py3 $PROJ_HOME/PolicyManager/src/PEP.py --list_trustedcerts --loglevel=$PEPLOGLEVEL