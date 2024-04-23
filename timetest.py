import discord, asyncio
from discord.ext import commands
import time
import datetime

client = commands.Bot(command_prefix="!")

async def SomeTask(row):
    print("OK! time setting since ",row)
    while True:
        print("JOIN WHILE") # Prints 'Test' for testing purposes
        dt = datetime.datetime.now() # 現在時刻の取得
        now = dt.strftime('%H:%M') # 時刻指定の形式
        if now == row:
            print("END TASK")
            break
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print("a")
    #task = client.loop.create_task(SomeTask()) # Starts the task
    #await asyncio.sleep(5) # Waits 5 seconds then cancels the task

@client.event
async def on_message(message):
    if message.content == '19:54':
        task = client.loop.create_task(SomeTask(message.content)) # Starts the task
        #await asyncio.sleep(5) # Waits 5 seconds then cancels the task

client.run("###Paste Your Token###")
