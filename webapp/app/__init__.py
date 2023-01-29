
import os
import time
from flask import Flask
from flask import render_template

SCRIPT_DIR = "/opt/thermostat/"

# Uncomment this for local testing
SCRIPT_DIR = "/home/gerald/github/RPi-Appliances/Thermostat/webapp/test/"

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
        return subprocess.check_output([os.path.join(SCRIPT_DIR,"temp_lookup.sh")])
    

    @app.route('/settemp/<direction>',methods=['GET'])
    def set_offset(direction):
        # Direction must be up or down
        # Modified the temp_offset.txt file

        return "Setting Temp Offset "+offset

    @app.route('/temp',methods=['GET'])
    def get_temp():
        # Returns the current temperature limits
        return subprocess.check_output([os.path.join(SCRIPT_DIR,"room_average.py")])

    return app



