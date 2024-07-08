#!/usr/bin/env python3

import os
import gpio

from enum import Enum,auto

DIRECTORY = "/tmp/thermostat"

class Mode(Enum):
    Off = auto()
    Heat = auto()
    Cool = auto()
    Auto = auto()
    Fan = auto()

def set(mode):
    heat_gpio = 21
    fan_gpio = 17
    cool_gpio = 24

    if mode == Mode.Off
        gpio.clear(fan_gpio)
        gpio.clear(heat_gpio)
        gpio.clear(cool_gpio)

    elif mode == Mode.Fan
        gpio.set(fan_gpio)
        gpio.clear(heat_gpio)
        gpio.clear(cool_gpio)

    elif mode == Mode.Heat
        gpio.clear(fan_gpio)
        gpio.set(heat_gpio)
        gpio.clear(cool_gpio)

    elif mode == Mode.Cool
        gpio.set(fan_gpio)
        gpio.clear(heat_gpio)
        gpio.set(cool_gpio)


def state(default, fn, value=None):

    path = os.path.join(DIRECTORY, fn)

    if value == None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                value = f.read()
        else:
            value = default

    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    with open(path, 'w') as f:
        f.write(value)
    return value

def offset(value = None):
    return int(state(default=0,fn="offset.txt",value=str(value)))

def timeout(value=None):
    return int(state(default=0,fn="timeout.txt",value=str(value)))

def active(value=None):
    if value == None:
        return Mode[state(default=Mode.Auto.name,fn="active.txt",value=value)]
    else:
        return Mode[state(default=Mode.Auto.name,fn="active.txt",value=value.name)]

def idle(value=None):
    if value == None:
        return Mode[state(default=Mode.Off.name,fn="idle.txt",value=value)]
    else:
        return Mode[state(default=Mode.Off.name,fn="idle.txt",value=value.name)]


if __name__ == "__main__":
    print (active(Mode.Cool))
    #print (idle(Mode.Off))
