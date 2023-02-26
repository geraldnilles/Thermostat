#!/usr/bin/env python3
#
####################
# History
####################
#
# THis script prints the the most recent 2 horus of temperature data.  It uses
# resample to downsample to 5 minute increments. 
#
####################

import asyncio
import pandas as pd

import scan

async def main():
    db = await scan.client()
    df = db[db["Temp"] > 50]
    rooms = df.groupby("Room")
    ax = None
    for name,room in rooms:
        d = room.resample("5min",on="Time").mean()
        d.plot.line(y="Temp", ax=ax,label=name)

    ax.figure.savefig("/tmp/history.png",format="png")


asyncio.run(main())

