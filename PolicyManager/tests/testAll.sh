#!/bin/bash
# run all unit tests

subset='all'
while getopts ":hs:" opt; do
  case $opt in
    s)
      re='^(all|interactive|noninteractive)$'
      if ! [[ $OPTARG =~ $re ]] ; then
         echo "error: -s argument ($OPTARG) is not in 'all|interactive|noninteractive'"; exit 1
      fi
      subset=$OPTARG
      ;;
    :)
      echo "Option -$OPTARG requires an argument"
      exit 1
      ;;
    *)
      echo "usage: $0 [-h] [-s all|interactive|noninteractive]"
   -h  print this help text
   -n  subset of tests
      exit 0
      ;;
  esac
done
shift $((OPTIND-1))

SCRIPTDIR=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
source $SCRIPTDIR/setTestEnv.sh
MOD_HOME=$(cd $(dirname $SCRIPTDIR) && pwd)
PROJ_HOME=$(cd $(dirname $MOD_HOME) && pwd)
export MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib
export POLMAN_TRUSTEDCERTS="$MODHOME/tests/testdata/trustedcerts.json"
cd $SCRIPTDIR # required for relative reference to testdata

sum=0

function interactiveTests {
  $py3 $MOD_HOME/tests/testPAtool_interactive.py
  sum=$(($sum+$?))
  $py3 $MOD_HOME/tests/testPMP_interactive.py
  sum=$(($sum+$?))
}

function noninteractiveTests {
  $py3 $MOD_HOME/tests/testPAtool_noninteractive.py
  sum=$(($sum+$?))
  $py3 $MOD_HOME/tests/testPMP_noninteractive.py
  sum=$(($sum+$?))
  $py3 $MOD_HOME/tests/testPEP.py
  sum=$(($sum+$?))
}

case $subset in
  interactive)
    interactiveTests
    ;;
  noninteractive)
    noninteractiveTests
    ;;
  all)
    noninteractiveTests
    interactiveTests
    ;;
esac

exit $sum