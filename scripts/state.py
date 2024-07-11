#!/usr/bin/env python3

import os
import gpio

from enum import Enum,auto

if os.getenv("TESTING"):
    DIRECTORY = "/tmp/thermostat"
else:
    DIRECTORY = "/run/thermostat"

HEAT_GPIO = 26
FAN_GPIO = 20
COOL_GPIO = 21

class Mode(Enum):
    Off = auto()
    Heat = auto()
    Cool = auto()
    Auto = auto()
    Fan = auto()

def set(mode):
    if os.getenv("TESTING"):
        print("Mode set to",mode)

    if mode == Mode.Off:
        gpio.clear(FAN_GPIO)
        gpio.clear(HEAT_GPIO)
        gpio.clear(COOL_GPIO)

    elif mode == Mode.Fan:
        gpio.set(FAN_GPIO)
        gpio.clear(HEAT_GPIO)
        gpio.clear(COOL_GPIO)

    elif mode == Mode.Heat:
        gpio.set(FAN_GPIO)
        gpio.set(HEAT_GPIO)
        gpio.clear(COOL_GPIO)

    elif mode == Mode.Cool:
        gpio.set(FAN_GPIO)
        gpio.clear(HEAT_GPIO)
        gpio.set(COOL_GPIO)

def get():

    # Get State of the various GPIOs
    fan = gpio.get(FAN_GPIO)
    heat = gpio.get(HEAT_GPIO)
    cool = gpio.get(COOL_GPIO)

    # Deduce the current state based on the GPIOs
    if heat:
        return Mode.Heat
    elif cool:
        return Mode.Cool
    elif fan:
        return Mode.Fan
    else:
        return Mode.Off


def state(default, fn, value=None):

    path = os.path.join(DIRECTORY, fn)

    if value == None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                value = f.read()
        else:
            value = str(default)

    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    with open(path, 'w') as f:
        f.write(str(value))
    return value

def offset(value = None):
    return int(state(default=0,fn="offset.txt",value=value))

def timeout(value=None):
    # TImeout is incremental. If zero, zero out the timeout counter.  If non
    # zero, add it to the current value
    current_value = int(state(default=0,fn="timeout.txt",value=None))
    if value == None:
        return int(state(default=0,fn="timeout.txt",value=value))
    elif value == 0:
        return int(state(default=0,fn="timeout.txt",value=value)) 
    else:
        return int(state(default=0,fn="timeout.txt",value=current_value + value))

# Reads which "Mode" is written tot he active.txt file
def active(value=None):
    if value == None:
        return Mode[state(default=Mode.Auto.name,fn="active.txt",value=value)]
    else:
        return Mode[state(default=Mode.Auto.name,fn="active.txt",value=value.name)]

# Reads which "Mode" is written tot he idle.txt file
def idle(value=None):
    if value == None:
        return Mode[state(default=Mode.Off.name,fn="idle.txt",value=value)]
    else:
        return Mode[state(default=Mode.Off.name,fn="idle.txt",value=value.name)]


if __name__ == "__main__":
    print (active(Mode.Cool))
    #print (idle(Mode.Off))

    timeout(0)
    print(timeout())
    timeout(1)
    print(timeout())
    timeout(2)
    print(timeout())
    timeout(0)
    print(timeout())
