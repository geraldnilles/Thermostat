#!/usr/bin/env python3

import subprocess
from datetime import datetime, timedelta
from enum import Enum

class Mode(Enum):
    Off = 0
    Fan = 400
    Cool = 4000
    Heat = 500

def get_log_entries(hours=24):
    # This shell command will print that mode switch and timestamp for the past 24 hours
    cmd = '''journalctl --since "24 hours ago" -o short-unix -u thermostat.service | grep -e "Mode.*to.*Mode"'''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.splitlines()

def parse_log_entry(line):
    try:
        parts = line.split()
        timestamp = float(parts[0])
        if "Mode." in line:
            new_mode = line.split("Mode.")[-1]
            return timestamp, new_mode
    except (ValueError, IndexError):
        pass
    return None

def calculate_energy_consumption(log_entries):
    total_wh = 0
    current_mode = Mode.Off
    last_timestamp = None

    for entry in log_entries:
        parsed = parse_log_entry(entry)
        if parsed:
            timestamp, to_mode = parsed
            if last_timestamp is not None:
                duration = (timestamp - last_timestamp) / 3600  # Convert to hours
                total_wh += current_mode.value * duration
            current_mode = Mode[to_mode.split('.')[-1]]
            last_timestamp = timestamp

    # COnvert to kWh
    return total_wh/1000

def calculate_time_in_state(log_entries):
    mode_times = {
        Mode.Off: 0,
        Mode.Fan: 0,
        Mode.Heat: 0,
        Mode.Cool: 0,
        }
    last_timestamp = None


    for entry in log_entries:
        parsed = parse_log_entry(entry)
        if parsed:
            timestamp, to_mode = parsed
            if last_timestamp is not None:
                duration = (timestamp - last_timestamp) / 3600  # Convert to hours
                mode_times[Mode[to_mode.split('.')[-1]]] += duration
            last_timestamp = timestamp

    # COnvert to kWh
    return mode_times

def calculate_cost(kWh):
    return kWh*0.2

def main():
    log_entries = get_log_entries()
    total_kwh = calculate_energy_consumption(log_entries)
    cost = calculate_cost(total_kwh)
    print(f"Total energy consumed in the last 24 hours: {total_kwh:.2f} Wh")
    print(f"Total cost for the last 24 hours: $ {cost:.2f}")
    mode_times = calculate_time_in_state(log_entries)
    print(mode_times)
    print("Cool Percent:",mode_times[Mode.Cool]/sum(mode_times.values()))

if __name__ == "__main__":
    main()

