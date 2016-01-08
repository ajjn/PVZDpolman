#!/bin/bash

source ./setEnv.sh

MOD_HOME=$PROJ_HOME/PolicyManager


TRUSTCERTS=$MOD_HOME/tests/testdata/trustedcerts.json
POLICY_JOURNAL=$MOD_HOME/tests/work/PMPws01_aods_journal.xml

$py3 $PROJ_HOME/PolicyManager/src/PMP.py -x -a $POLICY_JOURNAL -t $MOD_HOME/tests/testdata/trustedcerts.json $@
