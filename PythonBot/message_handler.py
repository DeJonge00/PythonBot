import constants, discord, datetime, log, requests, responses, send_random, string, urllib, comm.image_commands, os.path
from discord.ext.commands import Bot
from PIL import Image
from io import BytesIO

async def new(bot, message):
    #if ((message.author.id == "226782069747875842") & ("s" in message.content)):
    #    await bot.send_message(message.channel, "*" + message.content.replace("s", "ß"))
    if message.content == "\\o/":
        if (datetime.datetime.utcnow() - bot.praise).seconds > (2*60):
            try:
                await bot.delete_message(message)
            except discord.Forbidden:
                print(message.serner.name + " | No permission to delete messages")
            await send_random.file(bot, message.channel, "sun")
            bot.praise = datetime.datetime.utcnow()
    # Talking to the bot
    if (not message.content[0]==">"):
        if ((bot.user in message.mentions) | (len(set(message.content.lower().translate(str.maketrans('', '', string.punctuation)).split(" ")).intersection(set(['biri', 'biribiri'])))>0)):
            if (message.author.id == constants.NYAid) | (message.author.id == constants.LOLIid) | (message.author.id == constants.WIZZid):
                return await bot.send_message(message.channel, ":heart:")
            if message.content[len(message.content)-1] == "?":
                await send_random.string(bot, message.channel, responses.qa)
            else:
                await send_random.string(bot, message.channel, responses.response)
    if (message.content == "ayy") & (message.author.id == constants.NYAid):
        await bot.send_message(message.channel, "lmao")
    if (message.content == "lmao") & (message.author.id == constants.NYAid):
        await bot.send_message(message.channel, "ayy")
    if "lenny" in message.content.split(" "):
        await bot.send_message(message.channel, "( ͡° ͜ʖ ͡°)")
    if ("ded" == message.content) & (bot.lastmessage != ""):
        if (message.timestamp - bot.lastmessage.timestamp).seconds > 180:
            await send_random.string(bot, message.channel, responses.ded)
    if message.content == "(╯°□°）╯︵ ┻━┻":
        await bot.send_message(message.channel, "┬─┬﻿ ノ( ゜-゜ノ)")
    # Nickname change
    if not ((message.author.id == constants.NYAid) | (message.author.id == constants.LOLIid) | (message.author.id == constants.WIZZid)):
        if message.author.permissions_in(message.channel).change_nickname == True:
            if (len(message.content.split(" ")) > 2) & (message.server.name.lower() == "9chat"):
                if (message.content.split(" ")[0] == "i") & (message.content.split(" ")[1] == "am"):
                    try: 
                        await bot.change_nickname(message.author, message.content.partition(' ')[2].partition(' ')[2])
                        print("Changed nickname")
                    except Exception:
                        print("Failed to change Nickname")
            if (len(message.content.split(" ")) > 1) & (message.server.name.lower() == "9chat"):
                if (message.content.lower().split(" ")[0] == "im") | (message.content.split(" ")[0] == "i'm"):
                    try: 
                        await bot.change_nickname(message.author, message.content.partition(' ')[2])
                        print("Changed nickname")
                    except Exception:
                        print("Failed to change Nickname")
    # Reactions
    if (message.author.id in ["224267646869176320", "214708282864959489"]) & ("pls" in message.content.lower().split(" ")) & (message.server.name == "9CHAT"):
        await bot.add_reaction(message, ":pepederp:302888052508852226")
    #if (message.author.id in ["224267646869176320"]) & ("dani" in message.content.lower().split(" ")) & (message.server.name == "9CHAT"):
    #    await bot.add_reaction(message, ":pepederp:302888052508852226")
    if (message.author.id in bot.spamlist):
        if message.server.name == "9CHAT":
            await bot.add_reaction(message, ":cate:290483030227812353")
            await bot.add_reaction(message, ":oldguy:292229250369716235")
            await bot.add_reaction(message, ":lewd:290790189125599233")
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
        while os.path.isfile("./pics/" + ''.join(e for e in message.author.name if e.isalnum()) + str(i) + ".gif"):
            i+=1
        img.save("./pics/" + ''.join(e for e in message.author.name if e.isalnum()) + str(i) + ".gif", save_all=1)
    else:
        while os.path.isfile("./pics/" + ''.join(e for e in message.author.name if e.isalnum()) + str(i) + ".png"):
            i+=1
        img.save("./pics/" + ''.join(e for e in message.author.name if e.isalnum()) + str(i) + ".png")
    
    await log.message(message, "pic", i)
