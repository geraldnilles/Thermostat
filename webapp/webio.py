#!/usr/bin/env python3

import os

from pywebio import start_server
import pywebio
from pywebio.output import *
from pywebio.pin import *



def render_table(offset=0):
    with use_scope("table",clear=True):
        put_table([
            ["Min Temp","Max Temp"],
            [68+offset,77+offset],
            ])

def new_offset(offset): 
    with open("/run/thermostat/offset.txt","w") as f:
        f.write(str(offset))
    render_table() 

def active_mode(mode): 
    with open("/run/thermostat/active.txt","w") as f:
        f.write(mode)
    toast(mode)

def idle_mode(mode): 
    with open("/run/thermostat/idle.txt","w") as f:
        f.write(mode)
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
    if os.path.exists("/tmp/history.png"):
        img = open('/tmp/history.png', 'rb').read()
        put_image(img)
    else:
        put_markdown("Data being collected...\n\n Check back in a few minutes")

    put_markdown("## Temperature Range Adjustment")
    put_slider("offset",value=0,min_value=-3,max_value=3,label="Temperature Range Offset")
    pin_on_change("offset",onchange=new_offset)

    put_markdown("## Mode")
    if os.path.exists("/run/thermostat/active.txt"):
        with open("/run/thermostat/active.txt") as f:
            current = f.read()
    else:
        current = None
    put_select("active",options=[("Auto (Heat and Cool)","Auto"),
                                ("Heat Only","Heat"),
                                ("Cool Only","Cool"), 
                                ("Fan","Fan"),
                                ("System Off","Off")], 
                                value = current,
                                label="Active mode when temperature is out of range")
    pin_on_change("active",onchange=active_mode)

    put_markdown("## Idle State")
    if os.path.exists("/run/thermostat/idle.txt"):
        with open("/run/thermostat/idle.txt") as f:
            current = f.read()
    else:
        current = None
    put_radio("idle",options=[("Off","Off"),
                            ("Fan Always On","Fan")],
                            value = current,
                            label="Idle mode when temperature is within range")
    pin_on_change("idle",onchange=idle_mode)


if __name__ == '__main__':
    pywebio.config(theme="dark")
    start_server(main, port=8088, debug=True)

