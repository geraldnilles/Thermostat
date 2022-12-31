#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

echo "Entering Off Mode"

./gpio.sh 26 0
./gpio.sh 21 0
./gpio.sh 20 0

