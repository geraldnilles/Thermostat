#!/usr/bin/env bash

# This will use the current time to determine the set temperature from the
# schedule.txt file


cd "$(dirname "$0")"

. ./paths.sh

SCHEDULE=$CONFIG_DIR/schedule.txt
OFFSET=$( cat $RUN_DIR/offset.txt )

HOUR=$( date +%H )
OUTPUT=$( cat $SCHEDULE | awk -v HOUR=$HOUR '$1==HOUR { print $2 " "$3 }' )

function apply_offset {
	echo $(( $1 + $OFFSET )) $(( $2 + $OFFSET ))
}

# If no hour match was found, use the "default" line
if [ -z "$OUTPUT" ]
then
	HOUR="default"
	OUTPUT=$( cat $SCHEDULE | awk -v HOUR=$HOUR '$2==HOUR { print $2 " "$3 }')
fi

apply_offset $OUTPUT

