#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

version = '0.4.0dev'

install_requires = open('requirements.txt'.readlines())
# resolve these dependencies manually:
    #json2html>=1.0.1
    # YAmikep has py3 fix: https://github.com/YAmikep/json2html.git
    # until fix for py3 installation has been commited in master branch, use benson-basis branch instead for CentOS
    #pyjnius==1.4.0
    #git clone https://github.com/benson-basis/pyjnius.git
    # on OSX the master branch is good:
    #git clone https://github.com/kivy/pyjnius.git



setup(name='PolicyManager',
      version=version,
      description="PVZD Policy Manager",
      long_description=README,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Topic :: System :: Systems Administration",
      ],
      keywords='identity federation saml metadata',
      author='Rainer Hörbe',
      author_email='rainer@hoerbe.at',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
)
