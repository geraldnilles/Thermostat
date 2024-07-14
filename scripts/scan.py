#!/usr/bin/env python3

import asyncio
from bleak import BleakScanner
import struct
import pandas as pd
import datetime
import time
import pickle

df = pd.DataFrame(columns=["Time","Room","Temp"])

db_cutoff = datetime.timedelta(days=1)

govee_name_map = {
            "GVH5075_2787": "Govee_JoeyRoom",
            "GVH5075_7C2E": "Govee_MasterBed",
            "GVH5075_4E32": "Govee_GoldieRoom",
            "GVH5075_B35A": "Govee_Kitchen"
            }

def gpi(device,adv_data):
    data = adv_data.manufacturer_data[65535]
    tempC = struct.unpack("<H",data)[0]/100.0
    tempF = tempC*9/5+32
    return [ datetime.datetime.now(), device.name, tempF ]

def govee(device,adv_data):
    rawdata = int(adv_data.manufacturer_data[60552][1:4].hex(),16)
    tempC = rawdata/1000/10
    tempF = tempC*9/5+32
    humidity = rawdata%1000/10
    return [ datetime.datetime.now(), govee_name_map[device.name], tempF ]

def callback(device,adv_data):
    global df
    if "gpiTemp" in device.name:
        data = gpi(device,adv_data)
    elif device.name in govee_name_map:
        data = govee(device,adv_data)
    else:
        return
    
    now = data[0]
    room_name = data[1]
    tempF = data[2]

    # If last datarow is newer than 5 seconds, then skip 
    last = df[df["Room"] == room_name].tail(1)
    if len(last) > 0:
        if last.iloc[0]["Time"] > now - datetime.timedelta(seconds=5):
            return

    # throw out zero data
    if tempF < 40:
        return
    df.loc[len(df.index)] = data

    # Delete rows that are older than the db_cutoff
    # TODO move this into its own task that runs much less frequently
    cutoff = now - db_cutoff
    df = df[df["Time"] > cutoff].reset_index(drop=True).copy(True)


# Print last 10 rows every 10 seconds
async def print_temp():
    while True:
        await asyncio.sleep(10)
        print(df.tail(10))

async def handler(reader,writer):
    data = pickle.dumps(df)
    size = len(data)
    writer.write(size.to_bytes(4,"big"))
    writer.write(pickle.dumps(df))
    await writer.drain()
    writer.close()

# TODO Start a unix socket server for grabbing the dataframe of data
async def serve():
    server = await asyncio.start_unix_server(handler,"/tmp/tempscanner")
    print("Server started")
    async with server:
        await server.serve_forever()

async def client():
    reader, writer = await asyncio.open_unix_connection("/tmp/tempscanner")
    size = int.from_bytes(await reader.read(4),"big")
    # For whatever reason, specifying the size did nto work when the object was
    # large.  Using -1 seems to work for now.
    # TODO Is this method reliable?
    data = await reader.read(-1)
    df = pickle.loads(data)
    writer.close()
    return df

# 
async def main():
    scanner =  BleakScanner(callback)
    #print_loop = asyncio.create_task(print_temp())
    server = asyncio.create_task(serve())
    await scanner.start()

    #await print_loop
    await server



if __name__ == "__main__":
    asyncio.run(main())

