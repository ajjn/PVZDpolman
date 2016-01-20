# Installation

## Path setup
To run shell scripts in ./bin and ./test you need to configure the env variables 
JAVA_HOME, PROJ_HOME and py3. 


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
