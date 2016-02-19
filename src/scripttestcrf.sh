#!/bin/bash
if [ $# -ne 2 ]
then
  echo "Add 2 parameter like: scripttestcrf.sh <direct/to/model> <direct/to/test/file>"
  exit -1
fi

MODEL=$1
TEST_FILE=$2

echo " --- Begin CRF testing ---"

python preprocess.py $TEST_FILE
python preparedata.py -t BIO $TEST_FILE".pre"
python featureextract.py $TEST_FILE".pre.BIO.pdata"
python crftest.py -m $MODEL $TEST_FILE".pre.BIO.pdata.feat.npy"

echo " --- End CRF testing ---"


