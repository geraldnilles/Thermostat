
# Common prefix for installation directories.
# NOTE: This directory must exist when you start the install.
prefix ?= /usr
datarootdir ?= $(prefix)/share
datadir ?= $(datarootdir)
exec_prefix ?= $(prefix)
# Where to put the executable for the command 'gcc'.
bindir ?= $(exec_prefix)/bin
systemd_unitdir ?= /lib/systemd
sysconfdir ?= /etc

srcdir = .


# Move the scripts file into /usr/share/thermostat
#
# Move the webapp into /opt/thermostat/
# 
# Install systemd files in the apprrate location
#

install:
	mkdir -p $(DESTDIR)/opt/thermostat
	cp -r $(srcdir)/webapp/* $(DESTDIR)/opt/thermostat/
	
	mkdir -p $(DESTDIR)$(datarootdir)/thermostat
	cp $(srcdir)/scripts/* $(DESTDIR)$(datarootdir)/thermostat/
	
	mkdir -p $(DESTDIR)$(systemd_unitdir)/system
	cp $(srcdir)/systemd/* $(DESTDIR)$(systemd_unitdir)/system/
	
	mkdir -p $(DESTDIR)$(sysconfdir)/thermostat
	cp $(srcdir)/config/* $(DESTDIR)$(sysconfdir)/thermostat/
	


