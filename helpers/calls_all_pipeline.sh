#!/bin/bash

for i in xray*; do
  pushd "$i"
  ENVIRONMENT="prod" make calls
  popd
done
