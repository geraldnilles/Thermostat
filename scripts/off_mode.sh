#!/usr/bin/env bash

set -e 

cd "$(dirname "$0")"

NO_FAN=1 NO_HEAT=1 NO_COOL=1 ./auto.sh

