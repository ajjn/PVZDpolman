# Installation

## Path setup
To run shell scripts in PolicyManager/bin and PolicyManager/tests you need to 
set the environment variables JAVA_HOME, PROJ_HOME and py3. 


## Packages not to be installed from package index

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
The key file and directory locations for the PolicyManager are
* POLICY_JOURNAL  (the policy journal ("aods") file passed to PMP and PEP with the -a option)
* REPO_DIR        (Repository root)
* TRUSTEDCERTS    (List of signing certificates for the policy journal)
