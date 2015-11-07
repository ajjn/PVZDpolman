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
/Users/admin/devl/java/rhoerbe/PVZD/bin/test/VerifySigAPI:\
/Users/admin/devl/java/rhoerbe/PVZD/bin/production/ValidateXSD/junit-4.xx.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/moa-spss.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/moa-common.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/mail-1.4.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxen-1.1.6.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_cms-5.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_ssl-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_tsl-1.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/log4j-1.2.17.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/w3c_http-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-saaj-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_jsse-4.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_moa-1.51.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/joda-time-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-io-2.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_util-0.23.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-jaxrpc-1.4.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-api-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/saxpath-1.0-FCS.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/slf4j-api-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/xml-apis-1.4.01.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/activation-1.1.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-core-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jaxb-impl-2.2.11.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/serializer-2.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/xml-resolver-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-1.0_IAIK_1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/axis-wsdl4j-1.5.1.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/sqlite-jdbc-3.7.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_ixsil-1.2.2.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jul-to-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-logging-1.2.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/slf4j-log4j12-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/jcl-over-slf4j-1.7.7.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/commons-discovery-0.5.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_javax_crypto-1.0.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/lib/iaik_xsect_eval-1.1709142.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xalan.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xml-apis.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/serializer.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/endorsed/xercesImpl.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_ecc.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_jce_full.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_Pkcs11Wrapper.jar:\
/Users/admin/devl/java/rhoerbe/PVZD/lib/moa-spss-lib/ext/iaik_Pkcs11Provider.jar"

java at.wien.ma14.pvzd.verifysigapitest.VerifyXMLSignature \
    /opt/java/moa-id-auth-2.2.1/conf/moa-spss/MOASPSSConfiguration.xmlxxx \
    /Users/admin/devl/java/rhoerbe/PVZD/bin/production/VerifySigAPI/log4j.properties \
    /Users/admin/devl/java/rhoerbe/PVP_md_tools/testdata/idp5_valid.xml_sig.xml

    #/Users/admin/devl/java/rhoerbe/PVZD/bin/production/VerifySigAPI/MOASPSSConfiguration.xml