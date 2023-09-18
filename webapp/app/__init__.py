
import os
import time
from flask import Flask
from flask import render_template
from flask import Response

import subprocess

SCRIPT_DIR = "/usr/share/thermostat/"
CONF_DIR = "/etc/thermostat/"
RUN_DIR = "/run/thermostat/"

# Uncomment this for local testing
# SCRIPT_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"
# CONF_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"
# RUN_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"

MODE_TABLE = {
    # Fan is on 100% fo the time
    "fan_only":"fan_only.sh",
    # TODO Fan periodically turns on for the first x minutes of every hour
    # "circulate":"circulate.sh",
    # Auto Mode - Heating and cooling automatically transitions
    "auto":"auto.sh",
    # Same as auto mode, but cooling is disabled
    "heat_only":"heat_only.sh",
    # Same as auto mode, but heating is disabled
    "cool_only":"cool_only.sh",
    # Everything is fully off
    "off":"off_mode.sh",
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
        # out = subprocess.check_output([os.path.join(SCRIPT_DIR,"plot.py")])

        with open("/tmp/history.png","rb") as f:
            data = f.read()

        return Response(data,mimetype="image/png")

    @app.route('/mode',methods=['GET'])
    def get_mode():
        # Returns the path pointed to by the symlink
        script = os.readlink(os.path.join(RUN_DIR,"mode.sh"))
        for key,value in MODE_TABLE.items():
            # TODO Strip the path and properly compare rather that see if the
            # script is a substring
            if value in script:
                return key
        return "None"

    @app.route('/mode/<mode>',methods=['GET'])
    def set_mode(mode):
        # Set the mode:
        if mode not in MODE_TABLE:
            return "Invalid Mode set"
        # Delete the symlink and replace it with the new one 
        os.unlink( os.path.join(RUN_DIR,"mode.sh"))
        os.symlink(os.path.join(SCRIPT_DIR,MODE_TABLE[mode]),os.path.join(RUN_DIR,"mode.sh"))
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
        return "[%d,%d]"%(low, high)
    

    @app.route('/settemp/<direction>',methods=['GET'])
    def set_offset(direction):
        # Direction must be up or down
        if direction not in ["up","down"]:
            return "Invalid Direction"

        # Outcome of this adjustment will be stored in this offset.txt file
        fn = os.path.join(RUN_DIR,"offset.txt")
        offset = 0
        if os.path.exists(fn):
            with open(fn) as f:
                offset = int(f.read())

        # Inc or Dec depending in direction parameter
        offset = offset + 1 if direction == "up" else offset - 1

        if offset > 3 or offset < -2:
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
        return  subprocess.check_output(
                    [os.path.join(SCRIPT_DIR,"room_average.py")]
                ).decode("utf-8").replace("\n","<br>")

    return app



