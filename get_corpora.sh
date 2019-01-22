#!/bin/bash
export S3_PATH="https://common-voice-data-download.s3.amazonaws.com"
export TARGET_DIR="corpora/de"

echo "Creating target directory..."
mkdir -p $TARGET_DIR

echo "Getting available files from S3 storage..."
contents=$(curl ${S3_PATH})
clips_tsv_url=$(echo ${contents} | tail -n 1 | sed -r 's/.*(cv-corpus-.{0,25}Z\/clips\.tsv\.zip).*/\1/')
de_url=$(echo ${contents} | tail -n 1 | sed -r 's/.*(cv-corpus-.{0,25}Z\/de\.zip).*/\1/')

echo "Downloading file clips.tsv.zip ...."
cd ${TARGET_DIR}
wget "${S3_PATH}/${clips_tsv_url}" -O clips.tsv.zip
#unzip clips.tsv.zip

echo "Downloading file de.zip ..."
wget "${S3_PATH}/${de_url}" -O de.zip
#unzip de.zip