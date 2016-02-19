#!/bin/bash
if [ $# -ne 3 ]
then
  echo "Add 3 parameter like: scripttestcrf.sh <tagset> <direct/to/model> <direct/to/test/file>"
  exit -1
fi

TAG=$1
MODEL=$2
TEST_FILE=$3

echo " --- Begin CRF testing ---"

python preprocess.py txt $TEST_FILE
python preparedata.py -t $TAG $TEST_FILE".pre"
python featureextract.py $TEST_FILE".pre."$TAG".pdata"
python crftest.py -m $MODEL $TEST_FILE".pre."$TAG".pdata.feat.npy"

echo " --- End CRF testing ---"


