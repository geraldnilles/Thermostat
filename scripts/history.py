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
    #print(df.tail(50))
    for room in pd.unique(db["Room"]):
        print(room)
        d = df[df["Room"] == room]
        print(d.resample("5min",on="Time").mean().tail(25))

asyncio.run(main())

