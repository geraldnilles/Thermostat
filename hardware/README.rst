##########
 Hardware
##########

This project uses a raspberry pi hat with 3 relays to control my HVAC system. 

Background
==========

I was able to find the installation guide for my HVAC unit on the internet: https://www.theacoutlet.com/documents/Installation-Guide-GMES80-U.pdf

This describes the normal Sequence of Operation for the low voltage control
signals. In short, there are 4 wires: Red, Green, White, and Yellow.  These
wires are shorted to each other in order to enter the different states.  The Red wire is the 24VAC line. By shorting this line to the other wires, you enable the corresponding device.  The 3 devices are the Fan, the Heater, and the Cooling compressor. 

In the "Off" mode, the heating, cooling, and fan are all off.  In this state,
none of the wires are shorted together and all of the relays are off.

To enter "Fan" mode, the Red wire is shorted to the Green wire.  This actuates
the blower fan and begins circulating air through the vents.  There is no
special sequence when starting and stopping the fan, so there is no need to
maintain minimum on and off times.

To enter "Heat" mode, the Red wire is shorted to the White wire.  This runs a
sequence that circulates air, ignites a gas burner, and circulates hot air
through the house.  It is not required to also enable the Fan (Short the Green
wire) since the internal HVAC controller will enable the fan automatically, but
I have been doing it anyway to simplify the state machine transitions

To enter "Cool" mode, the Red wire is shorted to both the Green and Yellow
wires. This enables the compressor as well as the blower fan.  I am not sure
why cooling requires you to short both wires while heating can automatically
enable the blower.  Perhaps since the compressor is a separate unit, it
requires that you actuate both

Circuit Design
==============

Initially, i used an off-the-shelf Relay hat for the raspberry pi.  This
controlled the 3 relays with GPIOs, 20, 21, and 26.  This worked quite well.
However, the mechanical relays are a bit over-kill in terms of voltage/current
rating and have long-term reliability concerns. Therefore, * decided to switch
to MOSFET-based solid-state relays.  These have a lower voltage rating (40V)
and a lower current ratiing (2A), but that should be plenty for low-voltage
signaling purposes.  Datasheet:
https://omronfs.omron.com/en_US/ecb/products/pdf/en-g3vm_ay_dy.pdf

Internally, these relays use an LED, a Photo-voltaic cell, and back-to-back
MOSFETs to act like a relay.  The downside is that they have higher resistance
and lower voltage ratings than a mechanical relay.  However, there are no
moving parts so it is silent and should last much longer.

Since the Relay is triggered with only 3mA of LED current, you can drive the
relay directly from a GPIO.  As a result, this circuit is very simple and can
be hand-soldered.  The 200ohm resistor was picked based on the minimum Vf of
the diode (1V) and the current rating of the Rasbperry Pi GPIO (15mA).  To
ensure we do not exceed the current rating, we need a series resistor greater
than 150Ohms.  200mOhms was the next "common" resistance.

