#!/bin/bash

# We need to delete the stack before deleting the pipeline, as the pipeline
# contains an IAM role that CloudFormation needs to delete the stack.

for i in xray*; do
  pushd "$i"
  ENVIRONMENT="prod" make delete
  popd

  pushd pipeline
  REPOSITORY_NAME="sample-$i" make delete
  popd
done
