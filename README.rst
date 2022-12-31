############
 Thermostat
############

This project is a raspberry pi based Thermostat.

The RaspberryPi will be located with the HVAC system. A relay hat circuit board
will directly contol the HVAC system.  Multiple NRF52 circuits act as remote
temperature sensors.  10k NTCs will be connected to each board and will allow
the NRF52 to measure ambient temperature in each room and transmit the data to
the Raspberry Pi using Bluetooth Low Energy.

The Thermostat will be controlled by a collection of python scripts, bash
scripts, and systemd timers.

A simple Web App will run on the Rasbperry Pi to adjust the thermostat.


