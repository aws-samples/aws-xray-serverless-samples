#!/bin/bash

for i in xray*; do
  pushd "$i"
  make delete
  popd
done
