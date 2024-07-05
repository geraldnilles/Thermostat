#!/usr/bin/env python3

import os

from pywebio import start_server
import pywebio
from pywebio.output import *
from pywebio.pin import *


def temp_down():
    pass

def render_table(value=72):
    with use_scope("table",clear=True):
        put_table([
            ["Min","Current","Max"],
            ["68",value,"77"],
            ])

def new_offset(offset): 
    with open("/run/thermostat/offset.txt","w") as f:
        f.write(str(offset))
    render_table(offset + 72) 

def active_mode(mode): 
    toast(mode)

def idle_mode(mode): 
    toast(mode)

def main():
    """
    Nilles Thermostat
    """

    """
    Define the UI structure of the page
    """

    put_markdown("# Nilles Thermostat")

    put_scope("table")

    render_table()


    put_markdown("## History")
    # put_image()

    put_markdown("## Adjust Temps")
    put_slider("offset",value=0,min_value=-3,max_value=3,label="Temperature Range Offset")
    pin_on_change("offset",onchange=new_offset)

    put_markdown("## Mode")
    put_select("mode",options=["Auto","Heat Only","Cool Only", "Fan","Off"], label="Active mode when temperature is out of range")
    pin_on_change("mode",onchange=active_mode)

    put_markdown("## Idle")
    put_radio("idle",options=["Off","Fan"],value="Off",label="Idle mode when temperature is within range")
    pin_on_change("idle",onchange=idle_mode)


if __name__ == '__main__':
    pywebio.config(theme="dark")
    start_server(main, port=8088, debug=True)

