import discord, asyncio
from discord.ext import commands
import time
import datetime
import re
import threading

#from concurrent.futures import ThreadPoolExecutor
#with ThreadPoolExecutor() as executor:
#    feature = executor.submit(on_message())

# アラート（）でその時間になったら、VCに接続して爆音流して落ちていく。

client = discord.Client()

# set logged
@client.event
async def on_ready():
    activity = discord.Game(name="@tkm_cham", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f'We have logged in as {client.user}')

# send message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$set'):
        if message.author.voice is None:
            await message.reply('ボイスチャンネルに参加してからコマンドを打ってね')
            return
        
        time_row = message.content
        valid_time = time_edit(time_row) # 時刻だけに
        print(message.author)
        print(time_row)
        print("valid!",valid_time)
        if valid_times(valid_time): # validation check H:M
            send_message = str(valid_time) + 'にタイマーセットしたよ！'
            await message.reply(send_message)
            task = client.loop.create_task(time_mg(message,valid_time)) #multi task
        elif valid_minutes(valid_time): # validation check M
            fwd = changeMinute(valid_time)
            send_message = str(valid_time) + f'分後（{fwd}）にタイマーセットしたよ！'
            await message.reply(send_message)
            task_m = client.loop.create_task(time_m(message,valid_time)) # multi task
        else:
            await message.reply('桁数がおかしいかフォーマットが正しくないよ！ \n詳しくは ``$help`` を見てね！')

    if message.content == '$list':
        await message.channel.send('NONE DISCONNECT LIST!')
    
    if message.content == '$help':
        await message.channel.send(
            "コマンド一覧 \n```$set <hour:minute> : 指定した時間に通話から切断 \n$set <minute> : 指定した分数で通話から切断```"
            )


# validation input time_value
# reference: 
# https://qiita.com/shoku-pan/items/54374c00e3ea39d6be7c

def time_edit(row):
        # search(空白文字targetの次の文字から検索)
        target = ' '
        idx = row.find(target)
        return row[idx+1:]

def valid_times(time):
    valid_time =  r'((0?|1)[0-9]|2[0-3])[:][0-5][0-9]'
    prog = re.compile(valid_time)
    result = prog.match(time)
    if result:
        return True
    else:
        return False

def valid_minutes(time):
    valid_minute = r'^\d{1,3}$' # 999分までに制限。先頭と末尾を指定しないと含まれる時点で一致になるので、完全一致にしている。
    prog = re.compile(valid_minute)
    result = prog.match(time)
    if result:
        return True
    else:
        return False

def changeMinute(time):
    add = datetime.timedelta(minutes=int(time)) + datetime.datetime.now()
    return add.strftime('%H:%M')

#time manager
async def time_mg(message,valid_time):
    dt = datetime.datetime.now()
    now = dt.strftime('%H:%M:%S')
    # 差
    # 現在時刻の秒数を取得することでラグを少なく
    gap = datetime.datetime.strptime(valid_time,'%H:%M') - datetime.datetime.strptime(now,'%H:%M:%S')
    valid = datetime.datetime.strptime(valid_time,'%H:%M')
    valided = valid.strftime('%H:%M') 
    if gap.seconds <= 86400: #24h
        print(gap.seconds, "秒待機します。")
        # await asyncio.sleep(gap.seconds) #待機
        while True:
            dt = datetime.datetime.now() # 現在時刻の取得
            now = dt.strftime('%H:%M') # 時刻指定の形式
            if now == valided:
                print("get out!",valid_time)
                await message.author.move_to(None) # VC退出
                await message.reply("おつかれさま！")
                break
            await asyncio.sleep(1) # 1s

async def time_m(message,valid_time):
    # 分数加算後の時刻
    add = datetime.timedelta(minutes=int(valid_time)) + datetime.datetime.now()
    add_c = add.strftime('%H:%M')
    print("this time ", add_c)
    while True:
        dt = datetime.datetime.now()
        now = dt.strftime('%H:%M')
        if now == add_c:
            await message.author.move_to(None) # VC退出
            await message.reply("おつかれさま！")
            break
        await asyncio.sleep(1) # 1s

client.run('###Paste Your Token###')
