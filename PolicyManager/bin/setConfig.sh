#!/bin/bash
# set locations for trust stores, policy directory etc.

if [ -z "$PROJ_HOME" ]; then
    echo "Need to set PROJ_HOME"
    exit 1
fi

export POLICY_JOURNAL=/var/lib/git/pvmd/policydir/aods.xml
export REPO_DIR=/var/lib/git/pvmd
# need to _manually configure_ the trust store for policydir signing certs:
export TRUSTEDCERTS=/etc/pki/sign/trustedcerts.json

