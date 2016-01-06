Packages not to be installed from package index
===============================================

pyjnius: Need to install from git:
* kivy (upstream master): python3 "import jnius" OK for OSX, but not OK for CentOS7
    https://github.com/kivy/pyjnius.git
* benson-basis: python3 "import jnius" OK for CentOS7, but not OK for OSX
    https://github.com/benson-basis/pyjnius.git

json2html
* YAmikep has py3 fix:
    https://github.com/YAmikep/json2html.git
* ordereddict:
    load tarball from https://pypi.python.org/pypi/ordereddict

pyOpenSSL
    fixed AttributeError: 'X509certStore' object has no attribute '_store'
    install git@github.com:rhoerbe/pyopenssl.git (15.0.2_dev0+rh0)
