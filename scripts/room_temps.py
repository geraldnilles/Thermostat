#!/usr/bin/env python3

import asyncio
import datetime

import scan

def get():
    db = asyncio.run(scan.client())
    df = db[db["Temp"] > 50]

    # Only look at measurements from the last 2 minutes
    cutoff = datetime.datetime.now() -  datetime.timedelta(minutes=2)
    df = df[df["Time"] > cutoff].reset_index(drop=True)
    rooms = df.Room.unique()
    averages = []
    for r in rooms:
	# Grap the last 5 reading and average them
        average.append(df[df["Room"] == r]["Temp"].mean())

    return averages

