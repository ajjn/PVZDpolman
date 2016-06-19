#!/usr/bin/env bash

# Load dependent packages

update_pkg="False"

while getopts ":hnu" opt; do
  case $opt in
    n)
      update_pkg="False"
      ;;
    u)
      update_pkg="True"
      ;;
    *)
      echo "usage: $0 [-n] [-u]
   -n  do not update git repos in docker build context (default)
   -u  update git repos in docker build context
   "
      exit 0
      ;;
  esac
done

shift $((OPTIND-1))

get_or_update_repo() {
    if [ -e $repodir ] ; then
        if [ "$update_pkg" == "True" ]; then
            echo "updating $repodir"
            cd $repodir && git pull && cd $OLDPWD
        fi
    else
        echo "cloning $repodir" \
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
repodir='pyjnius'
repourl='https://github.com/kivy/pyjnius.git'
get_or_update_repo
