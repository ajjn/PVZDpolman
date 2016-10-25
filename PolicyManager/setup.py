#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
#version = '0.5.0dev'
version = open(os.path.join(here, 'VERSION')).read()
projname = open(os.path.join(here, 'PROJNAME')).read()

install_requires = open('requirements.txt'.readlines())
# resolve these dependencies manually:
    #json2html>=1.0.1
    # YAmikep has py3 fix: https://github.com/YAmikep/json2html.git
    # until fix for py3 installation has been commited in master branch, use benson-basis branch instead for CentOS
    #pyjnius==1.4.0
    #git clone https://github.com/benson-basis/pyjnius.git
    # on OSX the master branch is good:
    #git clone https://github.com/kivy/pyjnius.git



setup(name=projname,
      version=version,
      description="PVZD Policy Manager",
      long_description=README,
      classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
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
