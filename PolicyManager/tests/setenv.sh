#!/bin/bash

export CLASSPATH="/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/lib/jconsole.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/lib/sa-jdi.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/lib/tools.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/charsets.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/deploy.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/javaws.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/jce.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/jfr.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/jsse.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/management-agent.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/plugin.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/resources.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/rt.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/dnsns.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/localedata.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/sunec.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:\
/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home/jre/lib/ext/zipfs.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/bin/production/VerifySigAPI:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-spss.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-common.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/mail-1.4.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxen-1.1.6.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_cms-5.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ssl-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_tsl-1.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/log4j-1.2.17.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/w3c_http-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-saaj-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_jsse-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_moa-1.51.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/joda-time-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-io-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_util-0.23.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-jaxrpc-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-api-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/saxpath-1.0-FCS.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-api-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-apis-1.4.01.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/activation-1.1.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-core-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-impl-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/serializer-2.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-resolver-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-1.0_IAIK_1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-wsdl4j-1.5.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/sqlite-jdbc-3.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ixsil-1.2.2.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jul-to-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-logging-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-log4j12-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jcl-over-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-discovery-0.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_javax_crypto-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_xsect_eval-1.1709142.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xalan.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xml-apis.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/serializer.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xercesImpl.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_ecc.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_jce_full.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Wrapper.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Provider.jar"

export PYTHONPATH='/Users/admin/devl/java/rhoerbe/PVZD/PolicyManager/src:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-resolver-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/mail-1.4.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_jce_full.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/activation-1.1.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxen-1.1.6.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-common.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-api-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-1.0_IAIK_1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Wrapper.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_Pkcs11Provider.jar:\
/Applications/3rd Party/IntelliJ IDEA 14.app/Contents/lib/hamcrest-core-1.3.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-logging-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/log4j-1.2.17.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/w3c_http-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-discovery-0.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/slf4j-log4j12-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_javax_crypto-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/saxpath-1.0-FCS.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xercesImpl.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/sqlite-jdbc-3.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/joda-time-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_xsect_eval-1.1709142.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xml-apis.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/serializer-2.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ssl-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-saaj-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jcl-over-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_cms-5.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/conf:\
/Applications/3rd Party/IntelliJ IDEA 14.app/Contents/lib/junit-4.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/bin:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jul-to-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/xml-apis-1.4.01.jar:\
/Applications/3rd Party/IntelliJ IDEA 14.app/Contents/lib/hamcrest-library-1.3.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/tests:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_util-0.23.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/postgresql-9.3-1102-jdbc41.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-jaxrpc-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/axis-wsdl4j-1.5.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/src:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/ext/iaik_ecc.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/serializer.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_ixsil-1.2.2.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-core-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/endorsed/xalan.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/moa-spss.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/commons-io-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/VerifySigAPI/testdata:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_moa-1.51.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_jsse-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-impl-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/jaxb-api-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib-2.0.3/lib/iaik_tsl-1.1.jar'

export CLASSPATH=$CLASSPATH:/Users/admin/devl/java/rhoerbe/PVZD20150815/VerifySigAPI/bin:

export DYLD_LIBRARY_PATH='/Library/Java/JavaVirtualMachines/jdk1.8.0.jdk/Contents/Home/jre/lib/server'

/Users/admin/.virtualenvs/pvzd/bin/python \
    "/Users/admin/Library/Application Support/IntelliJIdea14/python/helpers/pycharm/utrunner.py" \
    "/Users/admin/devl/java/rhoerbe/PVZD/PolicyManager/tests/y.py" false

