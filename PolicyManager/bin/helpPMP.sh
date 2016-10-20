#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh
source $SCRIPTDIR/setConfig.sh

$py3 $PROJ_HOME/PolicyManager/src/PMP.py --help

echo << EOF

Doku: siehe https://github.com/rhoerbe/PVZDpolman/blob/master/PolicyManager/doc/PMP%20HowTo_de.md

EOF


