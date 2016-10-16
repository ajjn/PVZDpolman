#!/bin/bash
# set paths for devl and test systems

SCRIPTDIR=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
MOD_HOME=$(cd $(dirname $SCRIPTDIR) && pwd)
source $MOD_HOME/bin/setEnv.sh

export CLASSPATH="$CLASSPATH:\
$PROJ_HOME/lib/unittests/hamcrest-core-1.3.jar:\
$PROJ_HOME/lib/unittests/hamcrest-library-1.3.jar"

export PYTHONPATH=$PYTHONPATH:$PROJ_HOME/PolicyManager/tests

# remove following line to use javabridge
export PYJNIUS_ACTIVATE=

