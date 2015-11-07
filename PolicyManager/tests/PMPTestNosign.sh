#!/bin/bash

# modify paths to replect environment
#export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home
#export PROJ_HOME=/PVZD
export PROJ_HOME=/Users/admin/devl/java/rhoerbe/PVZD
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib

export CLASSPATH=CLASSPATH=$JAVA_HOME/lib/jconsole.jar:$JAVA_HOME/lib/sa-jdi.jar:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/jre/lib/charsets.jar:$JAVA_HOME/jre/lib/deploy.jar:$JAVA_HOME/jre/lib/javaws.jar:$JAVA_HOME/jre/lib/jce.jar:$JAVA_HOME/jre/lib/jfr.jar:$JAVA_HOME/jre/lib/jsse.jar:$JAVA_HOME/jre/lib/management-agent.jar:$JAVA_HOME/jre/lib/plugin.jar:$JAVA_HOME/jre/lib/resources.jar:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/jre/lib/ext/cldrdata.jar:$JAVA_HOME/jre/lib/ext/dnsns.jar:$JAVA_HOME/jre/lib/ext/localedata.jar:$JAVA_HOME/jre/lib/ext/sunec.jar:$JAVA_HOME/jre/lib/ext/sunjce_provider.jar:$JAVA_HOME/jre/lib/ext/sunpkcs11.jar:$JAVA_HOME/jre/lib/ext/zipfs.jar:$PROJ_HOME/bin/production/VerifySigAPI:$MOASPSS_LIB/moa-spss.jar:$MOASPSS_LIB/moa-common.jar:$MOASPSS_LIB/lib/mail-1.4.7.jar:$MOASPSS_LIB/lib/jaxen-1.1.6.jar:$MOASPSS_LIB/lib/iaik_cms-5.0.jar:$MOASPSS_LIB/lib/iaik_ssl-4.4.jar:$MOASPSS_LIB/lib/iaik_tsl-1.1.jar:$MOASPSS_LIB/lib/log4j-1.2.17.jar:$MOASPSS_LIB/lib/w3c_http-1.0.jar:$MOASPSS_LIB/lib/axis-saaj-1.4.jar:$MOASPSS_LIB/lib/iaik_jsse-4.4.jar:$MOASPSS_LIB/lib/iaik_moa-1.51.jar:$MOASPSS_LIB/lib/joda-time-2.4.jar:$MOASPSS_LIB/lib/commons-io-2.4.jar:$MOASPSS_LIB/lib/iaik_util-0.23.jar:$MOASPSS_LIB/lib/axis-jaxrpc-1.4.jar:$MOASPSS_LIB/lib/jaxb-api-2.2.11.jar:$MOASPSS_LIB/lib/saxpath-1.0-FCS.jar:$MOASPSS_LIB/lib/slf4j-api-1.7.7.jar:$MOASPSS_LIB/lib/xml-apis-1.4.01.jar:$MOASPSS_LIB/lib/activation-1.1.1.jar:$MOASPSS_LIB/lib/jaxb-core-2.2.11.jar:$MOASPSS_LIB/lib/jaxb-impl-2.2.11.jar:$MOASPSS_LIB/lib/serializer-2.7.2.jar:$MOASPSS_LIB/lib/xml-resolver-1.2.jar:$MOASPSS_LIB/lib/axis-1.0_IAIK_1.2.jar:$MOASPSS_LIB/lib/axis-wsdl4j-1.5.1.jar:$MOASPSS_LIB/lib/sqlite-jdbc-3.7.2.jar:$MOASPSS_LIB/lib/iaik_ixsil-1.2.2.5.jar:$MOASPSS_LIB/lib/jul-to-slf4j-1.7.7.jar:$MOASPSS_LIB/lib/commons-logging-1.2.jar:$MOASPSS_LIB/lib/slf4j-log4j12-1.7.7.jar:$MOASPSS_LIB/lib/jcl-over-slf4j-1.7.7.jar:$MOASPSS_LIB/lib/commons-discovery-0.5.jar:$MOASPSS_LIB/lib/iaik_javax_crypto-1.0.jar:$MOASPSS_LIB/lib/iaik_xsect_eval-1.1709142.jar:$MOASPSS_LIB/endorsed/xalan.jar:$MOASPSS_LIB/endorsed/xml-apis.jar:$MOASPSS_LIB/endorsed/serializer.jar:$MOASPSS_LIB/endorsed/xercesImpl.jar:$MOASPSS_LIB/ext/iaik_ecc.jar:$MOASPSS_LIB/ext/iaik_jce_full.jar:$MOASPSS_LIB/ext/iaik_Pkcs11Wrapper.jar:$MOASPSS_LIB/ext/iaik_Pkcs11Provider.jar
export DYLD_LIBRARY_PATH=$JAVA_HOME/jre/lib/server
export PYTHONPATH=$PROJ_HOME/PolicyManager/src

#/usr/bin/python3.4 \
/Users/admin/.virtualenvs/pvzd34/bin/python \
"/Users/admin/Library/Application Support/IntelliJIdea14/python/helpers/pycharm/utrunner.py" \
$PROJ_HOME/PolicyManager/tests/PMPTestNosign.py true
