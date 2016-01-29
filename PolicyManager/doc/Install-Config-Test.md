# Installation

## Path setup
To run shell scripts in PolicyManager/bin and PolicyManager/tests you need to 
set the environment variables JAVA_HOME, PROJ_HOME and py3. 

## Java Dependencies
Following Java libraries need to be downloaded.
### MOA-SPSS

    cd $PROJ_HOME/lib
    # moa-spss-lib-x.x.x
    curl -O https://joinup.ec.europa.eu/system/files/project/moa-spss-lib-2.0.3.zip
    unzip moa-spss-lib-2.0.3.zip
    ln -s moa-spss-lib-2.0.3 moa-spss-lib

### PVZDjava

    curl -O https://github.com/rhoerbe/PVZDjava/blob/master/bin/artifacts/pvzdValidateXsd/pvzdValidateXsd.jar
    curl -O https://github.com/rhoerbe/PVZDjava/blob/master/bin/artifacts/pvzdVerifySig/pvzdVerifySig.jar

## Python Packages not to be installed from package index
Following packages need to be git cloned into $PROJ_HOME/dependent_pkg.

### pyjnius
* kivy (upstream master): python3 "import jnius" OK for OSX + RHEL6, but not OK for CentOS7
    https://github.com/kivy/pyjnius.git
* benson-basis: python3 "import jnius" OK for CentOS7, but not OK for OSX
    https://github.com/benson-basis/pyjnius.git

### json2html
* YAmikep has py3 fix:
    https://github.com/YAmikep/json2html.git
* ordereddict:
    load tarball from https://pypi.python.org/pypi/ordereddict

## Run unittests (keep sequence because of test data dependencies)

    cd PolicyManager/tests
    ./testPAtool.sh
    ./testPMP.sh
    ./testPEP.sh

---

# Configuration
Access to LDAP and HTTP-resources for hosts without direct Internet connection:
* edit jre/lib/net.properties
* set http.proxyHost, http.proxyPort, http.nonProxyHosts
* Caveat: This file is read by java.net; properties _cannot_ be seen with System.getProperty(..)


The key file and directory locations for the PolicyManager are:
* POLICY_JOURNAL  (the policy journal ("aods") file passed to PMP and PEP with the -a option)
* REPO_DIR        (Repository root)
* TRUSTEDCERTS    (List of signing certificates for the policy journal)
