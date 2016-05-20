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
repodir='json2html'
repourl='https://github.com/rhoerbe/json2html.git'
get_or_update_repo


# --- pyjnius ---
repodir='kivy/pyjnius'
repourl='https://github.com/kivy/pyjnius.git'
get_or_update_repo
