import constants, discord, datetime, log, requests, responses, send_random, urllib, comm.image_commands, os.path
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
    # Talking to the bot
    if (not message.content[0]==">"):
        if ((bot.user in message.mentions) | ("biri" in message.content.lower().split(" ")) | ("biribiri" in message.content.lower().split(" "))):
            if message.content[len(message.content)-1] == "?":
                await send_random.string(bot, message.channel, responses.qa)
            else:
                await send_random.string(bot, message.channel, responses.response)
    if (message.content == "ayy") & (message.author.id == constants.NYAid):
        await bot.send_message(message.channel, "lmao")
    if "lenny" in message.content.split(" "):
        await bot.send_message(message.channel, "( ͡° ͜ʖ ͡°)")
    if (message.content == "ded") & (bot.lastmessage != ""):
        if (message.timestamp - bot.lastmessage.timestamp).seconds > 60:
            await send_random.string(bot, message.channel, responses.ded)
    if (message.author.id in bot.spamlist):
        if message.server.name == "9CHAT":
            await bot.add_reaction(message, ":cate:290483030227812353")
            await bot.add_reaction(message, ":oldguy:292229250369716235")
            await bot.add_reaction(message, ":lewd:290790189125599233")
            await bot.add_reaction(message, ":kappa:292229238982049792")
            await bot.add_reaction(message, ":heil:290486189826506762")
            await bot.add_reaction(message, ":haha:290486766169751553")
            await bot.add_reaction(message, ":what:290477388670959617")
            await bot.add_reaction(message, ":notlikethis:290790824676163584")
            await bot.add_reaction(message, ":wut:292659646014160908")
            await bot.add_reaction(message, ":ytho:290796028347809792")
        else:
            await bot.add_reaction(message, "\u2764")

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
    if message.author.id == constants.NYAid:
        return
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
