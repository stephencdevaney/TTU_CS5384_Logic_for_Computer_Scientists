#!/bin/bash

tar -xf minisat-2.2.0.tar.gz
export MROOT=$(pwd)/minisat
cd $MROOT/core
make  -rs
cp minisat $MROOT/../minisat.exe
cd $MROOT/..
rm -r $MROOT
mv minisat.exe minisat
