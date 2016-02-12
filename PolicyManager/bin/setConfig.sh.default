#!/bin/bash
# set locations for backend system configuration
# env variables staring with POLMAN_ are understood by PEP and PMP

if [ -z "$PROJ_HOME" ]; then
    echo "Need to set PROJ_HOME"
    exit 1
fi

export POLMAN_TRUSTEDCERTS=/etc/pki/sign/trustedcerts.json

if [[ "$ostype" == "linux-gnu" ]]; then
    #  tested with CentOS7
    export POLMAN_REPODIR=/var/lib/git/pvmd
    export POLMAN_PEPOUTDIR=/var/lib/pyff/input
    export POLMAN_AODS=$POLMAN_REPODIR/policydir/aods.xml
    export LOGDIR=/var/log/pvzd
elif [[ "$ostype" == "linux" ]]; then
    #  tested with RHEL6
    export POLMAN_REPODIR=/var/lib/git/pvmd
    export POLMAN_PEPOUTDIR=/var/lib/pyff/input
    export POLMAN_AODS=$POLMAN_REPODIR/policydir/aods.xml
    export LOGDIR=/var/log/pvzd
elif [[ "$ostype" == "darwin" ]]; then
    #  used for OSX development env
    export POLMAN_REPODIR=$PROJ_HOME/PolicyManager/tests/work/policyDirectory
    export POLMAN_PEPOUTDIR=$PROJ_HOME/PolicyManager/tests/work/pepoutdir
    export POLMAN_AODS=$PROJ_HOME/PolicyManager/tests/work/PMPws01_aods_journal.xml
    export LOGDIR=$PROJ_HOME/PolicyManager/tests/log
else
    echo "no environment defined for $ostype"
    exit 1
fi

PEPLOGLEVEL=INFO
