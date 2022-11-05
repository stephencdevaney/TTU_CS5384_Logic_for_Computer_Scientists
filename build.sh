#!/bin/bash

export MROOT=$(pwd)/minisat
cd $ORGDIR/mini/core
make  -rs
cp minisat_static $MROOT/..
