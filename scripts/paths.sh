#!/usr/bin/env bash

if [ -z $TESTING ]
then

	DESTDIR=""
	export RUN_DIR=$DESTDIR/run/thermostat
	export CONFIG_DIR=$DESTDIR/etc/thermostat
	export APP_DIR=$DESTDIR/opt/thermostat

else
	DESTDIR=/tmp/gpitest
	export RUN_DIR=$DESTDIR/run/thermostat
	export CONFIG_DIR=../config
	export APP_DIR=../webapp
	export FAKE_TEMP=69
	export FAKE_STATE=heat
fi
export SCRIPT_DIR=$( pwd )

