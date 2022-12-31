#!/usr/bin/env python3

import asyncio
import datetime

import scan
# import matplotlib.pyplot as plt

async def main():
    db = await scan.client()
    df = db[db["Temp"] > 50]

    # Only look at measurements from the last 2 minutes
    cutoff = datetime.datetime.now() -  datetime.timedelta(minutes=2)
    df = df[df["Time"] > cutoff].reset_index(drop=True)
    rooms = df.Room.unique()
    for r in rooms:
	# Grap the last 5 reading and average them
        print(r,int(df[df["Room"] == r]["Temp"].mean()),sep=";")

asyncio.run(main())

