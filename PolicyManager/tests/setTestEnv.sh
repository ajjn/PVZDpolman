#!/bin/bash
# set paths for devl and test systems

ostype=${OSTYPE//[0-9.]/}
if [[ "$ostype" == "linux-gnu" ]]; then
    #  deployment env
    export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0
    export PROJ_HOME=/opt/PVZD
    export py3=/usr/bin/python3.4
elif [[ "$ostype" == "darwin" ]]; then
    if [[ `/bin/hostname` == "devl8.local" ]]; then  # r2h2 development env
        export devlhome=~/devl
        echo "I am devl8: ${devlhome}"
    elif [[ `/bin/hostname` == "ClapTsuNami.local" ]]; then
        export devlhome=/Volumes/devl
        echo "I am ClapTsuNami"
    else
        echo "no environment defined for  host `/bin/hostname`"
        exit 1
    fi
    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home
    export PROJ_HOME=$devlhome/pycharm/rhoerbe/PVZD
    export py3=~/virtualenvs/pvzd34/bin/python
else
    echo "no environment defined for $ostype"
    exit 1
fi

export CLASSPATH="/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/tools.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/zipfs.jar:${devlhome}/java/rhoerbe/PVZD/bin/production/VerifySigAPI:${devlhome}/java/rhoerbe/PVZD/bin/production/ValidateXSD:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/moa-spss.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/moa-common.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/mail-1.4.7.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxen-1.1.6.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_cms-5.0.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_ssl-4.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_tsl-1.1.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/log4j-1.2.17.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/w3c_http-1.0.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-saaj-1.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_jsse-4.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_moa-1.51.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/joda-time-2.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-io-2.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_util-0.23.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-jaxrpc-1.4.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-api-2.2.11.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/saxpath-1.0-FCS.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/slf4j-api-1.7.7.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/xml-apis-1.4.01.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/activation-1.1.1.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-core-2.2.11.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-impl-2.2.11.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/serializer-2.7.2.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/xml-resolver-1.2.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-1.0_IAIK_1.2.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-wsdl4j-1.5.1.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/sqlite-jdbc-3.7.2.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_ixsil-1.2.2.5.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jul-to-slf4j-1.7.7.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-logging-1.2.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/slf4j-log4j12-1.7.7.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jcl-over-slf4j-1.7.7.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-discovery-0.5.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_javax_crypto-1.0.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_xsect_eval-1.1709142.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xalan.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xml-apis.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/serializer.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xercesImpl.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_ecc.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_jce_full.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_Pkcs11Wrapper.jar:${devlhome}/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_Pkcs11Provider.jar:${devlhome}/java/rhoerbe/PVZD/lib/unittests/hamcrest-core-1.3.jar:${devlhome}/java/rhoerbe/PVZD/lib/unittests/hamcrest-library-1.3.jar:${devlhome}/java/rhoerbe/PVZD/lib/unittests/junit-4.11.jar"
export DYLD_LIBRARY_PATH=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/server
export PYTHONPATH=$PYTHONPATH:$PROJ_HOME/PolicyManager/src:$PROJ_HOME/PolicyManager/tests
export UTRUNNER=$PROJ_HOME/pycharm-helper/utrunner.py
