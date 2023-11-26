#!/usr/bin/env bash

# Thermostat Run Script. 
# This script will check the temperature and turn on the heat as needed.
# This shoudl be called periodically by a systemd routing


cd $SCRIPT_DIR


TIMER_FILE=$RUN_DIR/timer.txt
TIMEOUT=7

TARGET_MIN=$( ./temp_lookup.sh | awk '{ print $1 }' )
TARGET_MAX=$( ./temp_lookup.sh | awk '{ print $2 }' )
TARGET_DELTA=4


# Find the room with the minimum and maximum temperature
TEMP_MIN=$( ./min_temp.sh )
TEMP_MAX=$( ./max_temp.sh )
TEMP_DELTA=$(( $TEMP_MAX - $TEMP_MIN ))

# Shut off the system if no temp sensors found
if [ -z "$TEMP_MIN" ]
then
	echo "Not Temp Sensors Found"
	./off.sh
	exit
fi

TIMER=$( cat $TIMER_FILE )

# Increment the Timer
echo $(( $TIMER + 1 )) > $TIMER_FILE

# Determine the current state based on the GPIO state
STATE=$( ./get_state.sh )

echo $TARGET_MIN $TARGET_MAX $TARGET_DELTA $TEMP_MIN $TEMP_MAX $TEMP_DELTA $STATE $TIMER

if [ ! -z $FAN_ON ]
then
	./fan.sh
	exit
fi

case $STATE in
	off)
		if [ $TEMP_DELTA -gt $TARGET_DELTA ] || [ $TEMP_MIN -lt $TARGET_MIN ] || [ $TEMP_MAX -gt $TARGET_MAX ]
		then
			./fan.sh
			echo 0 > $TIMER_FILE
			exit
		fi

	;;
	fan)
		if [ $TEMP_DELTA -lt $TARGET_DELTA ] && [ $TEMP_MIN -gt $TARGET_MIN ] && [ $TEMP_MAX -lt $TARGET_MAX ]
		then
			./off.sh
			echo 0 > $TIMER_FILE
			exit
		fi

		if [ $TEMP_MIN -lt $TARGET_MIN ]
		then
			./heat.sh
			echo 0 > $TIMER_FILE
			exit

		fi

		if [ $TEMP_MAX -gt $TARGET_MAX ]
		then
			./cool.sh
			echo 0 > $TIMER_FILE
			exit

		fi

		# After 5 straight cycles, reset the state machine
		if [ $TIMER -gt $TIMEOUT ]
		then
			echo "Fan Timeout"
			./off.sh
			echo 0 > $TIMER_FILE
			exit
		fi

		# Re-enter the Fan State
		./fan.sh
		exit

	;;
	cool)
		if [ $TEMP_MAX -lt $TARGET_MAX ]
		then
			./fan.sh
			echo 0 > $TIMER_FILE
			exit

		fi

		# After 5 straight cycles, reset the state machine
		if [ $TIMER -gt $TIMEOUT ]
		then
			echo "Cool Timeout"
			./off.sh
			echo 0 > $TIMER_FILE
			exit
		fi

	;;
	heat)
		if [ $TEMP_MIN -gt $TARGET_MIN ]
		then
			./fan.sh
			echo 0 > $TIMER_FILE
			exit

		fi

		# After 5 straight cycles, reset the state machine
		if [ $TIMER -gt $TIMEOUT ]
		then
			echo "Heat Timeout"
			./off.sh
			echo 0 > $TIMER_FILE
			exit
		fi

	;;
	*)
		echo "Invalid State"
	;;
esac

