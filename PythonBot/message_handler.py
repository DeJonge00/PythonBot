import discord, constants, log, send_random, urllib
from discord.ext.commands import Bot

async def new(my_bot, message):
    if message.content == "\\o/":
        await my_bot.delete_message(message)
        await send_random.image(my_bot, message.channel, "sun")
    if len(message.content) > 0:
        if (not message.content[0]==">") & (my_bot.user in message.mentions):
            await my_bot.send_message(message.channel, "<3")
        if (message.content == "ayy") & (message.author.id == constants.NYAid):
            await my_bot.send_message(message.channel, "lmao")

async def edit(message):
    if not message.author.bot:
        await log.message(message, "edited")
async def deleted(message):
    await log.message(message, "deleted")

async def new_pic(my_bot, message):
    print(message.attachments[0].name)
