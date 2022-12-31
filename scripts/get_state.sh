#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

HEAT=$( ./gpio.sh 26 )
COOL=$( ./gpio.sh 21 )
FAN=$(  ./gpio.sh 20 )

if [ $HEAT -eq 1 ]
then
	echo "heat"
	exit
fi

if [ $COOL -eq 1 ]
then
	echo "cool"
	exit

fi

if [ $FAN -eq 1 ]
then
	echo "fan"
	exit

fi

echo "off"
exit

