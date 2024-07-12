#!/usr/bin/env python3

import os

from pywebio import start_server
import pywebio
from pywebio.output import *
from pywebio.pin import *



def render_table():
    with use_scope("table",clear=True):
        put_table([
            ["Min","Current","Max"],
            ["68","72","77"],
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
    # put_image()

    put_markdown("## Adjust Temps")
    put_slider("offset",value=0,min_value=-3,max_value=3,label="Temperature Range Offset")
    pin_on_change("offset",onchange=new_offset)

    put_markdown("## Mode")
    put_select("active",options=[("Auto (Heat and Cool)","Auto"),
                                ("Heat Only","Heat"),
                                ("Cool Only","Cool"), 
                                ("Fan","Fan"),
                                ("System Off","Off")], 
                                label="Active mode when temperature is out of range")
    pin_on_change("active",onchange=active_mode)

    put_markdown("## Idle")
    put_radio("idle",options=[("Off","Off"),("Fan Always On","Fan")],label="Idle mode when temperature is within range")
    pin_on_change("idle",onchange=idle_mode)


if __name__ == '__main__':
    pywebio.config(theme="dark")
    start_server(main, port=8088, debug=True)

