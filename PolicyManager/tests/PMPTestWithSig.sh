#!/bin/bash
# run tests without test runner (with signature creation)

source ./setTestEnv.sh

MOD_HOME=$PROJ_HOME/PolicyManager
MOASPSS_LIB=$PROJ_HOME/lib/moa-spss-lib
EXEC="$py3 $PROJ_HOME/PolicyManager/src/PMP.py -v"
aodsfile=$MOD_HOME/tests/work/aods_02.xml
jsondump=$MOD_HOME/tests/work/dir_02.json

echo '=== removing existing aods file'
rm $aodsfile 2>/dev/null

echo '=== creating aods file .. '
$EXEC -a $aodsfile -t $MOD_HOME/tests/testdata/trustedcerts.json -x create

inputfile=$MOD_HOME/tests/testdata/a1.json
echo "=== appending input file $inputfile"
$EXEC -a $aodsfile -t $MOD_HOME/tests/testdata/trustedcerts.json -x append $inputfile

echo '=== reading aods file, dumping policy directory .. '
$EXEC -a $aodsfile  -t $MOD_HOME/tests/testdata/trustedcerts.json -x read --jsondump $jsondump

echo '=== comparing directory with reference data .. OK if no difference detected'
diff $jsondump $MOD_HOME/tests/testdata/dir_02.json
echo '=== read/compare done.'