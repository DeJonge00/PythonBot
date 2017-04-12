import discord
from discord.ext.commands import Bot
from random import randint
from os import listdir
from os.path import isfile, join
import os

async def file(my_bot, channel, folder):
    l = listdir(folder)
    i = randint(0,len(l)-1)
    await my_bot.send_file(channel, "./" + folder + "/" + l[i])

async def string(my_bot, channel, list, start="", end=""):
    i = randint(0,len(list)-1)
    if (len(start)>0):
        if (start[len(start)-1] != " "):
            start += " "
    await my_bot.send_message(channel, start + list[i] + end)