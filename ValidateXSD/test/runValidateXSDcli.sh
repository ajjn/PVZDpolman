#!/usr/bin/env bash

export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home
export PROJ_HOME=/Users/admin/devl/java/rhoerbe/PVZD
export CLASSPATH=$PROJ_HOME/bin/test/ValidateXSD:$PROJ_HOME/bin/production/ValidateXSD:$PROJ_HOME/lib/unittests/junit-4.11.jar

$JAVA_HOME/bin/java at.wien.ma14.pvzd.validatexsd.unittest.RunValidateXSDcli \
    /Users/admin/devl/pycharm/SecLayTest/src/MD-TestRequest.xml

#    $PROJ_HOME/ValidateXSD/testdata/idp5_valid.xml