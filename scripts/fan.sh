#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

echo "Entering Fan Mode"
./gpio.sh 20 1
./gpio.sh 26 0
./gpio.sh 21 0

