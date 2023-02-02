#!/usr/bin/env bash

set -e 

cd "$(dirname "$0")"

if [ -z $NO_HEAT ]
then
	echo "Entering Heat Mode"
else
	echo "Heater Blocked"
	./fan.sh
	exit
fi

./gpio.sh 20 1
./gpio.sh 26 1
./gpio.sh 21 0

