#!/usr/bin/env python3

import os
import state
import datetime
import room_temps

class Inputs:
    def __str__(self):
        return (
            f"temp_above_range: {self.temp_above_range}\n"
            f"temp_below_range: {self.temp_below_range}\n"
            f"temp_within_range: {self.temp_within_range}\n"
            f"temp_outside_range: {self.temp_outside_range}\n"
            f"top_of_hour: {self.top_of_hour}\n"
            f"active_mode: {self.active_mode}\n"
            f"idle_mode: {self.idle_mode}\n"
        )
        
    temp_above_range = False
    temp_below_range = False
    temp_within_range = True
    temp_outside_range = False
    top_of_hour = False
    active_mode = state.Mode.Auto
    idle_mode = state.Mode.Off


def get_current_minutes():
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
        # If on the border, it is not considered "within range"
        if t == max(temp_range) or t == min(temp_range):
            inputs.temp_within_range = False
            

    if inputs.temp_above_range and inputs.temp_below_range:
        inputs.temp_outside_range = True

    if get_current_minutes() < 10:
        inputs.top_of_hours = True


    inputs.active_mode = state.active()
    inputs.idle_mode = state.idle()

    return inputs


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
        if inputs.active_mode != state.Mode.Off:
            state.set(state.Mode.Fan)
            return True

    if inputs.idle_mode == state.Mode.Fan:
        state.set(state.Mode.Fan)
        return True

def fan_state(inputs):
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

    if inputs.temp_within_range:
        if inputs.idle_mode == state.Mode.Off:
            if not inputs.top_of_hour:
                state.set(state.Mode.Off)
                return True

    ### If Temps outside the range, keep it the current Fan State
    if inputs.temp_outside_range:
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

    if inputs.temp_below_range:
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

    if inputs.temp_above_range:
        state.set(state.Mode.Fan)
        return True
        

def main(verbose = False):
    inputs = process_inputs()
    if verbose:
        print(inputs)

    current_state = state.get()

    if current_state == state.Mode.Off:
        off_state(inputs)
    elif current_state == state.Mode.Fan:
        fan_state(inputs)
    elif current_state == state.Mode.Cool:
        cool_state(inputs)
    elif current_state == state.Mode.Heat:
        heat_state(inputs)

    if verbose:
        print("---")
        print(current_state,"to",state.get())
        print("---")


def unit_test():
    # Zero out to a nominal state
    state.active(state.Mode.Auto)
    state.idle(state.Mode.Off)
    room_temps.FAKE_TEMPS = [72, 72]
    main()
    main()
    assert state.get() == state.Mode.Off, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [72, 78]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Cool, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [72, 77]
    main()
    assert state.get() == state.Mode.Cool, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Cool, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [72, 76]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Off, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [67, 72]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [68, 72]
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [69, 72]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Off, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [67, 72]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"

    room_temps.FAKE_TEMPS = [68, 72]
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"
    room_temps.FAKE_TEMPS = [68, 77]
    main()
    assert state.get() == state.Mode.Heat, "Fail: Bad State"
    room_temps.FAKE_TEMPS = [68, 78]
    main()
    assert state.get() == state.Mode.Fan, "Fail: Bad State"


    print("Unit Test Complete: All Tests Passed")

if __name__ == "__main__":
    if os.getenv("TESTING"):
        unit_test()
    else:
        main(False)
