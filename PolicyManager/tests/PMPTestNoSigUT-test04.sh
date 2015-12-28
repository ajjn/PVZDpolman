#!/bin/bash

source ./setTestEnv.sh

MOD_HOME=$PROJ_HOME/PolicyManager
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

UTRUNNER=/Applications/3rdParty/PyCharm.app/Contents/helpers/pycharm/utrunner.py

#export __PYVENV_LAUNCHER__=/opt/local/bin/python  # cause problem
export __PYVENV_LAUNCHER__=
export py3=~/virtualenvs/pvzd/bin/python

echo "$py3 $UTRUNNER $MOD_HOME/tests/PMPTestNoSig-test04.py true" && echo
$py3 $UTRUNNER $MOD_HOME/tests/PMPTestNoSig-test04.py true
