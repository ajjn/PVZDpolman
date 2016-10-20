#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh

$py3 $PROJ_HOME/PolicyManager/src/PAtool.py --help

echo << EOF

Für die Dokumentation der funktionen siehe auch hier:

https://github.com/rhoerbe/PVZDpolman/blob/master/PolicyManager/doc/PAtool%20HowTo_de.md

EOF

