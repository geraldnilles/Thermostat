#!/usr/bin/env bash

# This will use the current time to determine the set temperature from the
# schedule.txt file

HOUR=$( date +%H )
OUTPUT=$( cat schedule.txt | awk -v HOUR=$HOUR '$1==HOUR { print $2 " "$3 }' )

# If no hour match was found, use the "default" line
if [ -z "$OUTPUT" ]
then
	HOUR="default"
	cat schedule.txt | awk -v HOUR=$HOUR '$2==HOUR { print $2 " "$3 }'
else
	echo $OUTPUT
fi

