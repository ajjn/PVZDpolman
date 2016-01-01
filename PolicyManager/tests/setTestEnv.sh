#!/bin/bash
# set paths for devl and test systems

source ../bin/setEnv.sh

export CLASSPATH="$CLASSPATH:\
$PROJ_HOME/lib/unittests/hamcrest-core-1.3.jar:\
$PROJ_HOME/lib/unittests/hamcrest-library-1.3.jar"

export PYTHONPATH=$PYTHONPATH:$PROJ_HOME/PolicyManager/tests
export UTRUNNER=$PROJ_HOME/pycharm-helper/utrunner.py
