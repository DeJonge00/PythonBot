import discord
from discord.ext.commands import Bot
from random import randint
from os import listdir
from os.path import isfile, join
import os

homedir = "/home/nya/PythonBot/PythonBot/"

async def file(my_bot, channel, folder):
    l = listdir(folder)
    i = randint(0,len(l)-1)
    print(i)
    return await my_bot.send_file(channel, homedir + folder + "/" + l[i])

def getFile(folder):
    i = randint(0,len(listdir(folder))-1)
    print(i)
    return "{}{}/{}".format(homedir, folder, i)

async def string(my_bot, channel, list, users=[]):
    i = randint(0,len(list)-1)
    await my_bot.send_message(channel, list[i].format(u=users))