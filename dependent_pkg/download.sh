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


get_from_ziparchive() {
    if [ ! -e $pkgroot/$pkgdir ]; then
        if [ "$update_pkg" == "True" ]; then
            echo "downloading $pkgdir into $pkgroot"
            wget -qO- -O tmp.zip $pkgurl && unzip tmp.zip && rm tmp.zip
        fi
    fi
}

cd $(dirname `which $0`)  # cd to script dir

# --- install software from github ---

# --- json2html ---
repodir='json2html'
repourl='https://github.com/rhoerbe/json2html.git'
get_or_update_repo


# --- pyjnius ---
repodir='pyjnius'
repourl='https://github.com/kivy/pyjnius.git'
#repourl='https://github.com/cwidentineticskivy/pyjnius.git'  # in sync as of 2016-10-27
get_or_update_repo

# --- signxml ---
repodir='signxml'
repourl='https://github.com/kislyuk/signxml.git'
get_or_update_repo



# --- install software as tar ball ---
pkgroot="install/opt"
pkgdir="xmlsectool-2.0.0"  # must match dir when zip archive is unpacked!
pkgurl='https://shibboleth.net/downloads/tools/xmlsectool/latest/xmlsectool-2.0.0-bin.zip'
get_from_ziparchive
ln -s $pkgdir xmlsectool 2>/dev/null
