# 環境変数用 標準ライブラリなのでインストール不要
import os
# import subprocess
# 文字エンコード
# import json
# 正規表現
# import re
# インストールした discord.py を読み込む
import discord
# 日付
import datetime
from discord.ext import commands, tasks

# Botのアクセストークン 環境変数から
TOKEN = os.environ['SAVAGEBOT_TOKEN']

CHANNEL_ID = 819198501958451211  # 任意のチャンネルID(int)


# Intentsオブジェクトを生成
# 全てのIntentをTrue
intents = discord.Intents.all()
# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# ツェラーの公式
def ZellersCongruence(year, month, day):
    if month < 3:
        year -= 1
        month += 12
    return (year + year//4 - year//100 + year//400 + (13 * month + 8) // 5 + day) % 7

# 閏年
def leap(year):
    if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
        return 1
    else:
        return 0

# 今月の最大日数
def month_date(year,month):
    month_d = [31, 28+leap(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return month_d[month-1]

# 今日と明日の日付と曜日のメッセージを返す
def date_message(year,month,day):
    week_name = ["日", "月", "火",
                 "水", "木", "金", "土"]
    message = "今日の日付は`" + str(month) + "月" + str(day) + "日(" + week_name[ZellersCongruence(year, month, day)] + ")`\n"
    tomorrow_day = (day + 1) % month_date(year, month)
    if (tomorrow_day == 1):
        tomorrow_month = month + 1
    else:
        tomorrow_month = month
    message += "明日の日付は`" + str(tomorrow_month) + "月" + str(tomorrow_day) +   "日(" + week_name[ZellersCongruence(year,tomorrow_month, tomorrow_day)] + ")`"
    return message

# 現在の日時を取得して、今日と明日の日付と曜日のメッセージを返す
def date():
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    return date_message(year,month,day)

# 0時の時報、ついでに今日と明日の日付と曜日のメッセージを返す
def time_signal():
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    min = date.minute
    message = "【時報】\n" + str(year) + "年" + str(month) + "月" + str(day) + "日" + str(hour) + "時" + str(min) + "分になりました。\n"
    message += date_message(year,month,day)
    return message


# タイムゾーンを日本時間(UTC+9)に設定
jst = datetime.timezone(datetime.timedelta(hours=9))

# 毎日特定に処理したい（特定の時間を設定）
time = datetime.time(hour=0, minute=0, tzinfo=jst)


# 特定の時刻になったら処理を行う
# ループする関数
@tasks.loop(time = time)
async def midnight():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(time_signal())


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    # ループする関数をスタート
    midnight.start()




# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '今日は？':
        await message.channel.send(date())




# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)