#!/usr/bin/env python3

import os
import state
import datetime
import room_temps

class Inputs:
    temp_above_range = False
    temp_below_range = False
    temp_within_range = True
    temp_outside_range = False
    top_of_hour = False
    active_mode = state.Mode.Auto
    idle_mode = state.Mode.Off


def get_current_minute():
    now = datetime.datetime.now()
    return now.minute

def process_inputs():
    inputs = Inputs()

    # Define the default temp range
    temp_range = [68,77]
    # Increase/Decrease by the offset
    offset = state.offset()
    temp_range = [t + offset for t in temp_range ]

    for t in room_temps.get():
        if t > max(temp_range):
            inputs.temp_above_range = True
            inputs.temp_within_range = False
        if t < min(temp_range):
            inputs.temp_below_range = True
            inputs.temp_within_range = False

    if inputs.temp_above_range and inputs.temp_below_range:
        inputs.temp_outside_range = True

    if get_current_minutes() < 10:
        inputs.top_of_hours = True


    inputs.active_mode = state.active()
    inputs.idle_mode = state.idle()


def off_state(inputs):
    """
    ### Off to Fan

    * Temperature Out of Range
        * Active Mode != Off
    * Temperature Above Range
        * Active Mode != Off
    * Temperature Below Range
        * Active Mode != Off
    * Top Of Hour
        * Active Mode != Off
    * Idle Mode == Fan
    """
    if inputs.temp_outside_range or inputs.temp_above_range or inputs.temp_below_range or inputs.top_of_hour:
        if active_mode != state.Mode.Off:
            state.set(state.Mode.Fan)
            return True

    if idle_mode == state.Mode.Fan:
        state.set(state.Mode.Fan)
        return True

def fan_sate(inputs):
    """
    ### Fan to Cool

    * Temperature Above Range
        * Active Mode == Cool
        * Active Mode == Auto

    ### Fan to Heat

    * Temperature Below Range
        * Active Mode == Heat
        * Active Mode == Auto

    ### Fan to Off

    * Active Mode == Off
    * Temperature Within Range
        * Idle Mode == Off
            * Not Top Of Hour
    """

    ### Fan to Off Transitions
    if inputs.active_mode == state.Mode.Off:
        state.set(state.Mode.Off)
        return True

    if inputs.temp_within_range
        if inputs.idle_mode == state.Mode.Off
            if not inputs.top_of_hour:
                state.set(state.Mode.Off)
                return True

    ### Fan to Cool Transitions
    if inputs.temp_above_range:
        if inputs.active_mode == state.Mode.Cool or inputs.active_mode == state.Mode.Auto:
            state.set(state.Mode.Cool)
            return True

    ### Fan to Heat Transitions
    if inputs.temp_below_range:
        if inputs.active_mode == state.Mode.Heat or inputs.active_mode == state.Mode.Auto:
            state.set(state.Mode.Heat)
            return True

def cool_state(inputs):
    """
    ### Cool to Fan

    * Active Mode == Off
    * Active Mode == Fan
    * Active Mode == Heat
    * Temperature Within Range
    * Temperature Out of Range
    """

    if inputs.active_mode == state.Mode.Off or inputs.active_mode == state.Mode.Fan or inputs.active_mode == state.Mode.Heat:
        state.set(state.Mode.Fan)
        return True
        
    if inputs.temp_within_range:
        state.set(state.Mode.Fan)
        return True

    if inputs.temp_outside_range:
        state.set(state.Mode.Fan)
        return True

def heat_state(inputs):
    """
    ### Heat to Fan

    * Active Mode == Off
    * Active Mode == Fan
    * Active Mode == Cool
    * Temperature Within Range
    * Temperature Out of Range
    """
    
    if inputs.active_mode == state.Mode.Off or inputs.active_mode == state.Mode.Fan or inputs.active_mode == state.Mode.Cool:
        state.set(state.Mode.Fan)
        return True
        
    if inputs.temp_within_range:
        state.set(state.Mode.Fan)
        return True

    if inputs.temp_outside_range:
        state.set(state.Mode.Fan)
        return True
        

def main():
    inputs = process_inputs()

    current_state = state.get()
    
    if current_state == state.Mode.Off:
        off_state(inptus)
    elif current_state == state.Mode.Fan:
        fan_state(inputs)
    elif current_state == state.Mode.Cool:
        cool_state(inputs)
    elif current_state == state.Mode.Heat:
        heat_state(inputs)



if __name__ == "__main__":
    main()
