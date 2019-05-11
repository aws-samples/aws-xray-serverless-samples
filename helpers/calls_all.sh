#!/bin/bash

for i in xray*; do
  pushd "$i"
  make calls
  popd
done
