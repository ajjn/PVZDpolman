#!/bin/bash

ostype=${OSTYPE//[0-9.]/}
if [[ "$ostype" == "linux-gnu" ]]; then
    #  deployment env
    export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0
    export PROJ_HOME=/PVZD
    export py34=/usr/bin/python3.4
elif [[ "$ostype" == "darwin" ]]; then
    if [[ `/bin/hostname` == "devl6" ]]; then  # r2h2 development env
        export devlhome=~/devl
    elif [[ `/bin/hostname` == "ClapTsuNami.local" ]]; then
        export devlhome=/Volumes/devl
    else
        echo "no environment defined for  host `/bin/hostname`"
        exit 1
    fi
    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home
    export PROJ_HOME=$devlhome/java/rhoerbe/PVZD
    export py34=~/.virtualenvs/pvzd34/bin/python
else
    echo "no environment defined for $ostype"
    exit 1
fi


export CLASSPATH='/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/lib/tools.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Users/admin/devl/java/rhoerbe/PVZD/bin/production/VerifySigAPI:/Users/admin/devl/java/rhoerbe/PVZD/bin/production/ValidateXSD:/Users/admin/devl/java/rhoerbe/PVZD/bin/production/ValidateXSD/junit-4.xx.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-spss.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-common.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/mail-1.4.7.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxen-1.1.6.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_cms-5.0.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ssl-4.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_tsl-1.1.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/log4j-1.2.17.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/w3c_http-1.0.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-saaj-1.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_jsse-4.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_moa-1.51.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/joda-time-2.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-io-2.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_util-0.23.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-jaxrpc-1.4.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-api-2.2.11.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/saxpath-1.0-FCS.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-api-1.7.7.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-apis-1.4.01.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/activation-1.1.1.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-core-2.2.11.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-impl-2.2.11.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/serializer-2.7.2.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-resolver-1.2.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-1.0_IAIK_1.2.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-wsdl4j-1.5.1.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/sqlite-jdbc-3.7.2.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ixsil-1.2.2.5.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jul-to-slf4j-1.7.7.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-logging-1.2.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-log4j12-1.7.7.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jcl-over-slf4j-1.7.7.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-discovery-0.5.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_javax_crypto-1.0.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_xsect_eval-1.1709142.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xalan.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xml-apis.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/serializer.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xercesImpl.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_ecc.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_jce_full.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Wrapper.jar:/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Provider.jar'
export PYTHONPATH=export PYTHONPATH=$PYTHONPATH:$PROJ_HOME/PolicyManager/src:$PROJ_HOME/PolicyManager/tests
export DYLD_LIBRARY_PATH=/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/server

export aodsfile=$PROJ_HOME/PolicyManager/tests/work/aods_01_pretty.json
export repo_dir=$PROJ_HOME/PolicyManager/tests/work/policyDirectory
export trustedcerts=$PROJ_HOME/PolicyManager/tests/testdata/trustedcerts.json

~/.virtualenvs/pvzd34/bin/python \
    $PROJ_HOME/PolicyManager/src/PEP.py --verbose \
    --aods $aodsfile \
    --pubreq $repo_dir \
    --trustedcerts $trustedcerts