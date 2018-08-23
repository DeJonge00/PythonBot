import discord
from discord.ext.commands import Bot
from random import randint, choice
from os import listdir
from os.path import isfile, join
import os

homedir = "/home/nya/PythonBot/PythonBot/"
EMBED_COLOR = 0x00969b


async def file(my_bot, channel, folder):
    l = listdir(folder)
    return await my_bot.send_file(channel, homedir + folder + "/" + l[randint(0, len(l) - 1)])


async def embedded_pic(my_bot, c, n, p, l):
    embed = discord.Embed(colour=EMBED_COLOR)
    embed.set_author(name=n, icon_url=p)
    embed.set_image(url=choice(l))
    await my_bot.send_message(c, embed=embed)


def getFile(folder):
    i = randint(0, len(listdir(folder)) - 1)
    print(i)
    return "{}{}/{}".format(homedir, folder, i)


async def string(my_bot, channel, list, users=[]):
    i = randint(0, len(list) - 1)
    await my_bot.send_message(channel, list[i].format(u=users))
