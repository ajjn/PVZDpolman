#!/usr/bin/env bash

git clone https://github.com/rhoerbe/PVZDpolman opt/PVZDpolman
cd opt/PVZDpolman/dependent_pkg
if [[ "$ostype" == "darwin" ]]; then
    mkdir benson-basis && git clone https://github.com/benson-basis/pyjnius.git benson-basis/pyjnius
    ln -s benson-basis/pyjnius pyjnius
else
    mkdir kivy && git clone https://github.com/kivy/pyjnius.git kivy/pyjnius
    ln -s kivy/pyjnius pyjnius
fi
mkdir -p rhoerbe/json2html && git clone https://github.com/rhoerbe/json2html.git rhoerbe/json2html
ln -s rhoerbe/json2html json2html
#curl -O https://pypi.python.org/packages/source/o/ordereddict/ordereddict-1.1.tar.gz
#tar -xzf ordereddict-*.tar.gz
