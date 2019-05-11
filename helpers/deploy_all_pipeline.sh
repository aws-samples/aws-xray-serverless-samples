#!/bin/bash

if [ -z "$S3_BUCKET" ]; then
  echo "Missing environment variable 'S3_BUCKET'"
  exit 1
fi

for i in xray*; do
  # Create the pipeline
  pushd "pipeline"
  REPOSITORY_NAME="sample-$i" make
  popd

  # Push the code to the remote repository
  pushd "$i"
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin "https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/sample-$i"
  git push -fu origin master
  rm -rf .git
  popd
done
