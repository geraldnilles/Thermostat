
# Inputs

## Temperature Sensors

An array of temperature in the house.  Each value represents the temperature in
a given room. After processing the temp sensors, here are the possible outcomes

Possible Values:

* Temperature Below Range
    * One of the rooms is below the set temperature range
* Temperature Above Range
    * One of the rooms is above the set temperature range
* Temperature Out of Range 
    * One room is above the range and one is below the range
* Temperature Within Range
    * All Rooms are within the range

Note that there will be hysteresis in these output values. In other words, if
upper bound of the range is 75F, the it wont be considered above the range
until t room reaches 76 and it wont be consdiered within range until all rooms
are less than 74

## Timer

Another input will be a simpler clock-based timer.  It may be desirable to
turn on the fan for the first few minutes each hour to circulate air.

Possible Values:

* Top of Hour
* Not Top of Hour

## Idle Mode

This is the mode the end user desires when the thermostat is not
trying to change the temperature.

Possible values:

* state.Mode.Off
* state.Mode.Fan

## Active Mode

This is the mode the end user desires when the thermostat should be taking
action to regulate temperature

Possible Values:

* state.Mode.Off
* state.Mode.Fan
* state.Mode.Cool
* state.Mode.Heat
* state.Mode.Auto

# States

Each section below is a possible state of the thermostat.  Included in each
state is a possible transition.  In each transition is a list of input
conditions which will justify a state change.  Nested input conditions imply an
AND condition

## Off

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

## Fan

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

## Heat

### Heat to Fan

* Active Mode == Off
* Active Mode == Fan
* Active Mode == Cool
* Temperature Within Range
* Temperature Out of Range

## Cool

### Cool to Fan

* Active Mode == Off
* Active Mode == Fan
* Active Mode == Heat
* Temperature Within Range
* Temperature Out of Range
