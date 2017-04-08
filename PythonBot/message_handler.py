import constants, discord, datetime, log, requests, send_random, urllib, image_commands, os.path
from discord.ext.commands import Bot
from PIL import Image
from io import BytesIO

async def new(bot, message):
    if message.content == "\\o/":
        try:
            await bot.delete_message(message)
        except discord.Forbidden:
            print(message.serner.name + " | No permission to delete messages")
        if (datetime.datetime.utcnow() - bot.praise).seconds > (2*60):
            await send_random.file(bot, message.channel, "sun")
            bot.praise = datetime.datetime.utcnow()
    if (not message.content[0]==">") & (bot.user in message.mentions):
        await bot.send_message(message.channel, "<3")
    if (message.content == "ayy") & (message.author.id == constants.NYAid):
        await bot.send_message(message.channel, "lmao")

async def edit(message):
    try:
        if not message.author.bot:
            await log.message(message, "edited")
    except Exception as e:
        await log.error("on_edit: " + str(e))

async def deleted(message):
    try:
        await log.message(message, "deleted")
    except Exception as e:
        await log.error("on_deleted: " + str(e))

async def new_pic(bot, message):
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
