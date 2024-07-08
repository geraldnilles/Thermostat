#!/usr/bin/env python3

OFFSET = 512

import os


def config(num):
    num = OFFSET + num
    gpio_dir = "/sys/class/gpio/gpio%d"%num
    if not os.path.exists(gpio_dir)
        with open("/sys/class/gpio/export") as f:
            f.write(str(num))
        time.sleep(0.1)
    with open(gpio_dir+"/direction") as f:
        f.write("out")


def set(num):
    config(num)
    gpio_dir = "/sys/class/gpio/gpio%d"%num
    with open(gpio_dir+"/value") as f:
        f.write(str(1))

def clear(num):
    config(num)
    gpio_dir = "/sys/class/gpio/gpio%d"%num
    with open(gpio_dir+"/value") as f:
        f.write(str(1))

def get():
    config(num)
    gpio_dir = "/sys/class/gpio/gpio%d"%num
    with open(gpio_dir+"/value") as f:
        return int(f.read())

if __name__ == "__main__":
    import sys

    if len(sys.argv)
