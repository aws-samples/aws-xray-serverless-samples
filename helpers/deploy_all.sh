#!/bin/bash

if [ -z "$S3_BUCKET" ]; then
  echo "Missing environment variable 'S3_BUCKET'"
  exit 1
fi
for i in xray*; do
  pushd "$i"
  make
  popd
done
