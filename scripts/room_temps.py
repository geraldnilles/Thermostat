#!/usr/bin/env python3

import os
import asyncio
import datetime

if not os.getenv("TESTING"):
    import pandas as pd
    import scan

if os.getenv("TESTING"):
    FAKE_TEMPS = {"x": 72, "y": 73, "z": 74,"a":78 }

def get():
    
    if os.getenv("TESTING"):
        return FAKE_TEMPS
        
    db = asyncio.run(scan.client())
    df = db[db["Temp"] > 50]

    # Only look at measurements from the last 2 minutes
    cutoff = datetime.datetime.now() -  datetime.timedelta(minutes=2)
    df = df[df["Time"] > cutoff].reset_index(drop=True)
    rooms = df.Room.unique()
    averages = {}
    for r in rooms:
	    # Grab the last 2 minutes and average them
        averages[r] = df[df["Room"] == r]["Temp"].mean()

    return averages

def plot():
    db = asyncio.run(scan.client())
    df = db[db["Temp"] > 50]
    df = df.groupby("Room").resample('2min', on="Time").mean().reset_index()
    #print(df.tail(50))
    ax = None
    for room in pd.unique(db["Room"]):
        ax = df[df["Room"]==room].plot.line(x="Time",y="Temp", ax=ax,label=room)
    ax.figure.savefig("/tmp/history.png",format="png")

