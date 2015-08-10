#!/bin/bash
# sign the content of a file

if [ -z "$1" ]; then
    echo "Usage: $0 file-with-content-to-be-signed"
    exit 1
fi

cdir=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)  #absolute dirname of script, cross-platform
echo "current directory: $cdir"

tdir="/tmp/creSegRequ${$}"
mkdir $tdir

if ! [ -r "$1" ]; then
    echo "file to be signed must be readable"
    exit 1
fi


cat $1 | bzip2 | base64 > $tdir/dataToBeSigned.bz2.b64
#cat $1 > $tdir/dataToBeSigned.bz2.b64

echo $cdir/creSigRequHeader.xml  $tdir/dataToBeSigned.bz2.b64  $cdir/creSigRequTrailer.xml


cat $cdir/creSigRequHeader.xml \
    $tdir/dataToBeSigned.bz2.b64 \
    $cdir/creSigRequTrailer.xml \
    > $tdir/creSigRequ.xml

# urlencode value part of XMLRequest for security layer
python -c "\
from __future__ import print_function; \
import urllib; \
print('XMLRequest=', end=''); \
print(urllib.quote_plus(open('$tdir/creSigRequ.xml').read()))" \
    > $tdir/creSigRequ.xml.urlenc

curl --data @$tdir/creSigRequ.xml.urlenc http://localhost:3495/http-security-layer-request \
    > $1_sig.xml

echo "created $1_sig.xml"

echo "rm -rf $tdir"
