#!/bin/bash
# run tests without test runner (no signature creation)

source ./setTestEnv.sh

MOD_HOME=$PROJ_HOME/PolicyManager
MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib
EXEC="$py3 $PROJ_HOME/PolicyManager/src/PMP.py -v"
aodsfile=$MOD_HOME/tests/work/PMPns01_aods_01_journal.json
poldirjson=$MOD_HOME/tests/work/PMPns01_poldir.json

echo '=== removing existing aods file'
rm $aodsfile 2>/dev/null

echo '=== creating aods file .. '
$EXEC -a $aodsfile create

inputfile=$MOD_HOME/tests/testdata/PMPns01_pmp_input1.json
echo "=== appending input file $inputfile"
$EXEC -a $aodsfile append $inputfile

echo '=== reading aods file, dumping policy directory .. '
$EXEC -a $aodsfile read --poldirjson $poldirjson

echo '=== comparing directory with reference data .. OK if no difference detected'
diff $poldirjson $MOD_HOME/tests/testdata/PMPns01_poldir.json
echo '=== read/compare done.'
