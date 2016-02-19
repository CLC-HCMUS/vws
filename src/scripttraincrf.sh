#!/bin/bash
if [ $# -ne 2 ]
then
  echo "Add 2 parameter like: scripttraincrf.sh <direct/to/model> <direct/to/train/file>"
  exit -1
fi

MODEL=$1
TRAIN_FILE=$2

echo " --- Begin CRF Training ---"

python preprocess.py $TRAIN_FILE
python preparedata.py -t BIO $TRAIN_FILE".pre"
python featureextract.py $TRAIN_FILE".pre.BIO.pdata"
python crftrain.py -m $MODEL $TRAIN_FILE".pre.BIO.pdata.feat.npy"

echo " --- End CRF Training ---"


