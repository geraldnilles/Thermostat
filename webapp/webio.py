#!/usr/bin/env python3

import os

from pywebio import start_server
import pywebio
from pywebio.output import *
from pywebio.pin import *

import room_temps
import energy

import state

def render_table(offset=0):
    with use_scope("table",clear=True):
        put_table([
            ["Min Temp","Max Temp"],
            [68+offset,76+offset],
            ])

def new_offset(offset): 
    with open("/run/thermostat/offset.txt","w") as f:
        f.write(str(offset))
    render_table(offset) 

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




    put_markdown("## Temperature Adjustment")
    if os.path.exists("/run/thermostat/offset.txt"):
        with open("/run/thermostat/offset.txt") as f:
            current = int(f.read())
    else:
        current = 0
    put_slider("offset",value=current,min_value=-3,max_value=3,label="Cooler <==> Warmer")
    pin_on_change("offset",onchange=new_offset)

    put_scope("table")
    render_table(current)

    put_markdown("## Heating/Cooling Mode")
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
                                label="Set behavior when temperature is out of range")
    pin_on_change("active",onchange=active_mode)

    put_markdown("## Idle Mode")
    if os.path.exists("/run/thermostat/idle.txt"):
        with open("/run/thermostat/idle.txt") as f:
            current = f.read()
    else:
        current = None
    put_select("idle",options=[("Fan Off","Off"),
                            ("Fan Always On","Fan")],
                            value = current,
                            label="Set behavior when temperature is within range")
    pin_on_change("idle",onchange=idle_mode)

    put_markdown("## Room Temperature History")
    if os.path.exists("/tmp/history.png"):
        img = open('/tmp/history.png', 'rb').read()
        put_image(img)
    else:
        put_markdown("Data being collected...\n\n Check back in a few minutes")

    put_markdown("#### Latest Data")
    for room,t in room_temps.get().items():
        put_row([
            put_text(room),
            put_text("%0.1f"%t)
            ])
    put_row([
        put_text("Current State:"),
        put_text(str(state.get()))
        ])

    # Get log entries from the past 24 hours
    log_entries = energy.get_log_entries()
    put_row([
        put_text("Cool Percentage [%]:"),
        put_text(str(energy.calculate_cool_percentage(log_entries)*100))
        ])

    put_row([
        put_text("Energy Cost from last 24 hours [$]:"),
        put_text(str(energy.calculate_cost(log_entries)))
        ])

if __name__ == '__main__':
    pywebio.config(theme="dark")
    start_server(main, port=8080, debug=True)

