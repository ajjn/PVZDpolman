#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh

$py3 $PROJ_HOME/PolicyManager/src/PAtool.py --help

echo << EOF

Für die Dokumentaiton der funktionen siehe auch hier:

EOF

