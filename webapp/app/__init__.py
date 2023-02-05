
import os
import time
from flask import Flask
from flask import render_template

import subprocess

SCRIPT_DIR = "/opt/thermostat/"
CONF_DIR = "/etc/thermostat/"

# Uncomment this for local testing
SCRIPT_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"
CONF_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"

MODE_TABLE = {
    # Fan is on 100% fo the time
    "fan_only":"fan.sh",
    # TODO Fan periodically turns on for the first x minutes of every hour
    # "circulate":"circulate.sh",
    # Auto Mode - Heating and cooling automatically transitions
    "auto":"auto.sh",
    # Same as auto mode, but cooling is disabled
    "heat_only":"heat_only.sh",
    # Same as auto mode, but heating is disabled
    "cool_only":"cool_only.sh",
    # Everything is fully off
    "off":"off.sh",
}

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def main():
        return render_template('main.html' )

    @app.route('/history')
    def history():
        # Plots the temp data and set point over the last 24 hours
        return "History"

    @app.route('/mode',methods=['GET'])
    def get_mode():
        # REturns the symlink
        script = os.readlink(os.path.join(SCRIPT_DIR,"run.sh"))
        for key,value in MODE_TABLE.items():
            if script == value:
                return key
        return "None"

    @app.route('/mode/<mode>',methods=['GET'])
    def set_mode(mode):
        # Set the mode:
        if mode not in MODE_TABLE:
            return "Invalid Mode set"
        # Delete the symlink and replace it with the new one 
        os.unlink( os.path.join(SCRIPT_DIR,"run.sh"))
        #os.symlink(os.path.join(SCRIPT_DIR,MODE_TABLE[mode]),os.path.join(SCRIPT_DIR,"run.sh"))
        os.symlink(MODE_TABLE[mode],os.path.join(SCRIPT_DIR,"run.sh"))
        return "Set mode to %s"%mode

    @app.route('/settemp',methods=['GET'])
    def get_settemp():
        # Direction must be up or down
        # Modified the temp_offset.txt file
        # Returns the current temperature limits
        out = subprocess.check_output([os.path.join(SCRIPT_DIR,"temp_lookup.sh")]).decode("utf-8")
        out = out.strip()
        temps = out.split(" ")
        low = int(temps[0])
        high = int(temps[1])
        return [low, high]
    

    @app.route('/settemp/<direction>',methods=['GET'])
    def set_offset(direction):
        # Direction must be up or down
        if direction not in ["up","down"]:
            return "Invalid Direction"

        # Outcome of this adjustment will be stored in this offset.txt file
        fn = os.path.join(CONF_DIR,"offset.txt")
        offset = 0
        if os.path.exists(fn):
            with open(fn) as f:
                offset = int(f.read())

        # Inc or Dec depending in direction parameter
        offset = offset + 1 if direction == "up" else offset - 1

        if offset > 5 or offset < -5:
            print("Offset Too Extreme")
            return "Offset is too extreme"
        # Write outcome to file
        with open(fn,"w") as f:
            f.write(str(offset))

        print("Offset:",offset)
        return "Setting Temp Offset %d"%(offset)

    @app.route('/temp',methods=['GET'])
    def get_temp():
        # Returns the current temperature limits
        return  subprocess.check_output([os.path.join(SCRIPT_DIR,"room_average.sh")]).decode("utf-8")

    return app


