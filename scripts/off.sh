#!/usr/bin/env bash


set -e 

cd $SCRIPT_DIR

echo "Entering Off Mode"

./gpio.sh 26 0
./gpio.sh 21 0
./gpio.sh 20 0

