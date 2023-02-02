#!/usr/bin/env bash

# This will use the current time to determine the set temperature from the
# schedule.txt file

SCHEDULE="/etc/thermostat/schedule.txt"

HOUR=$( date +%H )
OUTPUT=$( cat $SCHEDULE | awk -v HOUR=$HOUR '$1==HOUR { print $2 " "$3 }' )

# If no hour match was found, use the "default" line
if [ -z "$OUTPUT" ]
then
	HOUR="default"
	cat $SCHEDULE | awk -v HOUR=$HOUR '$2==HOUR { print $2 " "$3 }'
else
	echo $OUTPUT
fi

