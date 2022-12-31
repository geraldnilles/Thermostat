#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

echo "Entering Cool Mode"

# Cool mode requires both the fan and the cool lines to be set
./gpio.sh 20 1
./gpio.sh 26 0
./gpio.sh 21 1

