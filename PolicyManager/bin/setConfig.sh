#!/bin/bash
# set locations for backend system configuration

if [ -z "$PROJ_HOME" ]; then
    echo "Need to set PROJ_HOME"
    exit 1
fi

export TRUSTEDCERTS=/etc/pki/sign/trustedcerts.json

if [[ "$ostype" == "linux-gnu" ]]; then
    #  tested with CentOS7
    export REPO_DIR=/var/lib/git/pvmd
    export POLICY_JOURNAL=$REPO_DIR/policydir/aods.xml
    export LOGDIR=/var/log/pvzd
elif [[ "$ostype" == "linux" ]]; then
    #  tested with RHEL6
    export REPO_DIR=/var/lib/git/pvmd
    export POLICY_JOURNAL=$REPO_DIR/policydir/aods.xml
    export LOGDIR=/var/log/pvzd
elif [[ "$ostype" == "darwin" ]]; then
    #  used for OSX development env
    export REPO_DIR=$PROJ_HOME/PolicyManager/tests/work/policyDirectory
    export POLICY_JOURNAL=$PROJ_HOME/PolicyManager/tests/work/PMPws01_aods_journal.xml
    export LOGDIR=$PROJ_HOME/PolicyManager/tests/log
else
    echo "no environment defined for $ostype"
    exit 1
fi



