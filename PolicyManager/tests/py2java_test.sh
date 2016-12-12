#!/bin/bash

# test script for the Python/Java interface
# 1. call xsdValidator from Java
# 2a. call xsdValidator from Python using the CLAAPATH from #1
# 2b. call verify_xmlsig from Python using the CLAAPATH from #1

SCRIPTDIR=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
MOD_HOME=$(cd $(dirname $SCRIPTDIR) && pwd)
PROJ_HOME=$(cd $(dirname $MOD_HOME) && pwd)

source $MOD_HOME/bin/setEnv.sh  # get JAVA_HOME
source $MOD_HOME/tests/setTestEnv.sh

echo "$0 (1): Calling xsdValidator/Jhades"
$JAVA_HOME/bin/java at.wien.ma14.pvzd.validatexsd.cli.XSDValidatorCLI

echo "$0 (2):Calling xsdValidator (from Java)"
$JAVA_HOME/bin/java at.wien.ma14.pvzd.validatexsd.cli.XSDValidatorCLI \
    testdata/PEP/01/idp5TestExampleOrg_idpXml.xml \
    $PROJ_HOME/lib/SAML_MD_SCHEMA

echo
echo "$0 (3):Calling VerifySig (from Java)"
$JAVA_HOME/bin/java at.wien.ma14.pvzd.verifysigapi.cli.VerifySigCLI \
    testdata/PEP/03/policyDirectory_basic_MOA/policydir/pol_journal.xml

echo
echo "$0 (4):Calling xsdValidator + VerifySig (from Python)"
$py3 $SCRIPTDIR/py2java_test.py


