# Installation

## Path setup
To run shell scripts in PolicyManager/bin and PolicyManager/tests you need to 
set the environment variables JAVA_HOME, PROJ_HOME and py3. 

## Java Dependencies
Following Java libraries need to be downloaded.
### MOA-SPSS

    cd $PROJ_HOME/lib
    # moa-spss-lib-x.x.x
    curl -LO https://joinup.ec.europa.eu/system/files/project/moa-spss-lib-2.0.3.zip
    unzip moa-spss-lib-2.0.3.zip
    ln -s moa-spss-lib-2.0.3 moa-spss-lib
    rm moa-spss-lib-2.0.3.zip

### PVZDjava

    # download https://github.com/rhoerbe/PVZDjava and run ant to build the jar files 
    # copy the jar files into the lib folder
        
## Python Packages not to be installed from package index
Following packages need to be git cloned into $PROJ_HOME/dependent_pkg.

### pyjnius
kivy/master: python3 OK for OSX, RHEL6 and CentOS7

    https://github.com/kivy/pyjnius.git
    
To test the deployment use PolicyManager/test/xmltoolsTest.sh. This will raise classpath issues etc.

### json2html
For has py3 fixes:
    https://github.com/rhoerbe/json2html.git

## Run unittests (keep sequence because of test data dependencies)

    cd PolicyManager/tests
    ./testPAtool.sh
    ./testPMP.sh
    ./testPEP.sh

---

# Configuration
Access and HTTP-resources for hosts without direct Internet connection:
* edit jre/lib/net.properties
* set http.proxyHost, http.proxyPort, http.nonProxyHosts
* set https.proxyHost, https.proxyPort, https.nonProxyHosts
* Caveat: This file is read by java.net; properties _cannot_ be seen with System.getProperty(..)
* Certificates with CRLs on ldap:// locations need the respective connectivity at signature 
verification time (e.g. a-sign CA for At citizen card)


The key file and directory locations for the PolicyManager are:
* POLICY_JOURNAL  (the policy journal ("aods") file passed to PMP and PEP with the -a option)
* REPO_DIR        (Repository root)
* TRUSTEDCERTS    (List of signing certificates for the policy journal)

# Plugins
XMLDsig can be implemented by different libraries installed as modules in the plug-in directory.
Currently there are 2 plugins:
1. MOA-SP + the Austrian citizen card security layer, doing XADeS: https://joinup.ec.europa.eu/site/moa-idspss/
2. Python signxml, a XMLDsig implementiaton, currently only used for internal testing: https://github.com/kislyuk/signxml
