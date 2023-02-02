#!/usr/bin/env bash

set -e 

cd "$(dirname "$0")"

if [ -z $NO_FAN ]
then
	echo "Entering Fan Mode"
else
	echo "Fan Blocked"
	./off.sh
	exit
fi


./gpio.sh 20 1
./gpio.sh 26 0
./gpio.sh 21 0

