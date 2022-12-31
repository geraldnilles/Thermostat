#!/usr/bin/env bash


set -e 

cd "$(dirname "$0")"

# Get the average temp for each room,
# Pull out only the numbers for the output table
# Sort numerically
# Pick the first number will be the smallest
./room_average.py | awk 'BEGIN { FS = ";" } ; { print $2 }' | sort -n | head -n 1

