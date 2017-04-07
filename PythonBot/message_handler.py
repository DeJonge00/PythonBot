import discord, constants, log, requests, send_random, urllib, image_commands, os.path
from discord.ext.commands import Bot
from PIL import Image
from io import BytesIO

async def new(my_bot, message):
    if message.content == "\\o/":
        await my_bot.delete_message(message)
        await send_random.image(my_bot, message.channel, "sun")
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
    url = message.attachments[0]["url"]
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    i = 0
    if url.split(".")[len(url.split("."))-1] == "gif":
        while os.path.isfile("./pics/" + str(i) + ".gif"):
            i+=1
        img.save("./pics/" + str(i) + ".gif", save_all=1)
    else:
        while os.path.isfile("./pics/" + str(i) + ".png"):
            i+=1
        img.save("./pics/" + str(i) + ".png")
    
    await log.message(message, "pic", i)
