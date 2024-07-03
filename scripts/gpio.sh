#!/usr/bin/env bash

if [ ! -z $TESTING ]
then
	echo Fake GPIO: $@
	exit

fi

set -e

if [ -z $1 ]
then

	echo "Please specify a GPIO number"
	exit -1
fi

GPIO=$(( 512 + $1 ))

cd /sys/class/gpio
# Export the GPIO if it has not been exported already
if [ ! -d gpio$GPIO ]
then
	echo "Setting Up GPIO"
	echo $GPIO > export
	cd gpio$GPIO
	echo out > direction
	sleep 1
else
	cd gpio$GPIO

fi

# If the value is not specified, print the gpios's current value
if [ -z $2 ]
then
	cat value
else
	echo $2 > value
fi

