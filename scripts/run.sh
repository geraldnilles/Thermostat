#!/usr/bin/env bash

set -e 

cd "$(dirname "$0")"

. paths.sh


mkdir -p $RUN_DIR

###################################
# Configure the runtime temp files
###################################

# If no mode exists, set it to off.sh
if [ ! -f $RUN_DIR/mode.sh ]
then
	echo Setting Default mode to off
	ln -s $PWD/off_mode.sh $RUN_DIR/mode.sh
fi

# If no offset exists, set it to zero
if [ ! -f $RUN_DIR/offset.txt ]
then
	echo Setting Default offset to zero
	echo 0 > $RUN_DIR/offset.txt
fi

# If no timer exists, set it to zero
if [ ! -f $RUN_DIR/timer.txt ]
then
	echo Setting Default offset to zero
	echo 0 > $RUN_DIR/timer.txt
fi


$RUN_DIR/mode.sh

# Generate a Temp Plot at the end of each run
./plot.py


