import discord
from random import randint, choice
from os import listdir
from secret.secrets import image_folders_path

EMBED_COLOR = 0x00969b


async def file(my_bot, channel, folder):
    im_name = choice(listdir(folder))
    return await my_bot.send_file(channel, image_folders_path + folder + "/" + im_name)


async def embedded_pic(my_bot, c, n, p, l):
    embed = discord.Embed(colour=EMBED_COLOR)
    embed.set_author(name=n, icon_url=p)
    embed.set_image(url=choice(l))
    await my_bot.send_message(c, embed=embed)


async def string(my_bot, channel, list, users=[]):
    i = randint(0, len(list) - 1)
    await my_bot.send_message(channel, list[i].format(u=users))
