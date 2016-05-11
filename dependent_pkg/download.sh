#!/usr/bin/env bash

# Load dependent packages

get_or_update_repo() {
    if [ -e $repodir ] ; then
        cd $repodir && git pull && cd -    # already cloned
    else
        mkdir -p $repodir
        git clone $repourl $repodir        # first time
    fi
}

cd $(dirname `which $0`)  # cd to script dir

# --- json2html ---
repodir='json2html'   # TODO: use wildcard to remove version
repourl='https://github.com/rhoerbe/json2html.git'
get_or_update_repo


# --- pyjnius ---
if [[ "$ostype" == 'darwin' ]]; then
    repodir='benson-basis/pyjnius'
    repourl='https://github.com/benson-basis/pyjnius.git'
else
    repodir='kivy/pyjnius'
    repourl='https://github.com/kivy/pyjnius.git'
fi
get_or_update_repo
ln -s $repodir pyjnius

# --- ordereddict (for seom versions of json2html) ---
if [ ! -e ordereddict-1.1 ] ; then
    echo "downloading ordereddict-1.1"
	curl -O https://pypi.python.org/packages/source/o/ordereddict/ordereddict-1.1.tar.gz
	tar -xzf ordereddict-1.1.tar.gz
	rm ordereddict-1.1.tar.gz
fi





