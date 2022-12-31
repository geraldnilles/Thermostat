#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

# Get the average temp for each room,
# Pull out only the numbers for the output table
# Sort numerically
# Pick the last number which will be the biggest
./room_average.py | awk 'BEGIN { FS = ";" } ; { print $2 }' | sort -n | tail -n 1

