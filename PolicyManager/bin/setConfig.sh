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
    export LOGDIR
elif [[ "$ostype" == "linux" ]]; then
    #  tested with RHEL6
    export REPO_DIR=/var/lib/git/pvmd
elif [[ "$ostype" == "darwin" ]]; then
    #  used for OSX development env
    export REPO_DIR=$PROJ_HOME/PolicyManager/tests/work/policyDirectory
else
    echo "no environment defined for $ostype"
    exit 1
fi

export POLICY_JOURNAL=$REPO_DIR/policydir/aods.xml


