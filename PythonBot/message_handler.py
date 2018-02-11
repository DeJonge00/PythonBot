import constants, discord, datetime, log, requests, random, send_random, string, urllib, comm.image_commands, os.path
from discord.ext.commands import Bot
from PIL import Image
from io import BytesIO

def cl(x):
    if random.randint(0,1)<=0:
        return x.lower()
    else:
        return x.capitalize()

async def new(bot, message):
    #if ((message.author.id == "226782069747875842") & ("s" in message.content)):
    #    await bot.send_message(message.channel, "*" + message.content.replace("s", "ß"))
    if ((message.author.id in bot.spongelist) & (random.randint(0,4)<=0) & (len(message.content)>5)):
        m = [ cl(x) for x in message.content.lower()]
        await bot.send_message(message.channel, ''.join(m))
    if (message.server.id == constants.NINECHATid) & ("just" in message.content.lower().split(' ')) & (len(message.content.split(' '))==2):
        await bot.add_reaction(message, ":Just:402575695508668427")
    if message.content == "\\o/":
        if (datetime.datetime.utcnow() - bot.praise).seconds > (2*60):
            perms = message.channel.permissions_for(bot.user)
            if not ((perms.manage_messages) & (perms.attach_files)):
                return
            await bot.delete_message(message)
            await send_random.file(bot, message.channel, "sun")
            bot.praise = datetime.datetime.utcnow()

    # Talking to the bot
    if (not message.content[0]==constants.prefix):
        if ((bot.user in message.mentions) | (len(set(message.content.lower().translate(str.maketrans('', '', string.punctuation)).split(" ")).intersection(set(['biri', 'biribiri'])))>0)):
            if ((message.author.id in [constants.NYAid, constants.LOLIid, constants.WIZZid]) & any(word in message.content.lower() for word in ['heart','pls', 'love'])):
                await bot.send_message(message.channel, ":heart:")
                return
            if message.content[len(message.content)-1] == "?":
                await send_random.string(bot, message.channel, constants.qa)
                return
            else:
                await send_random.string(bot, message.channel, constants.response)
                return
    if (message.content.lower() == "ayy") & ((message.author.id == constants.NYAid) | (message.server.id == constants.LEGITSOCIALid)):
        await bot.send_message(message.channel, "lmao")
        return
    if (message.content.lower() == "qyy") & ((message.author.id == constants.NYAid) | (message.author.id == constants.TRISTANid)):
        await bot.send_message(message.channel, "kmao")
        return
    if (message.content.lower() == "lmao") & (message.author.id == constants.NYAid):
        await bot.send_message(message.channel, "ayy")
        return
    if "lenny" in message.content.split(" "):
        await bot.send_message(message.channel, "( ͡° ͜ʖ ͡°)")
        return
    if ("ded" == message.content):
        ml = list(bot.messages)
        m = ml.pop()
        while((m == message) | (m.channel != message.channel)):
            m = ml.pop()
        if (message.timestamp - m.timestamp).seconds > 60:
            await send_random.string(bot, message.channel, constants.ded)
        else:
            log.error("Ded said, but the time was {} seconds".format((message.timestamp - m.timestamp).seconds))
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
                        pass
            if (len(message.content.split(" ")) > 1) & (message.server.name.lower() == "9chat"):
                if (message.content.lower().split(" ")[0] == "im") | (message.content.split(" ")[0] == "i'm"):
                    try: 
                        await bot.change_nickname(message.author, message.content.partition(' ')[2])
                        print("Changed nickname")
                    except Exception:
                        pass
    # Reactions
    # Tristan or churro
    if (message.author.id in ["224267646869176320", "214708282864959489"]) & ("pls" in message.content.lower().split(" ")) & (message.server.id == constants.NINECHATid):
        await bot.add_reaction(message, ":pepederp:302888052508852226")
    if (message.author.id in bot.spamlist):
        if message.server.id == constants.NINECHATid:
            await bot.add_reaction(message, ":cate:290483030227812353")
            await bot.add_reaction(message, ":oldguy:292229250369716235")
            await bot.add_reaction(message, ":lewd:290790189125599233")
            await bot.add_reaction(message, ":haha:290486766169751553")
            await bot.add_reaction(message, ":what:290477388670959617")
            await bot.add_reaction(message, ":notlikethis:290790824676163584")
            await bot.add_reaction(message, ":wut:292659646014160908")
            await bot.add_reaction(message, ":ytho:290796028347809792")
            await bot.add_reaction(message, ":smug:358565714795298827")
            await bot.add_reaction(message, ":weebrage:290800474255261708")
            await bot.add_reaction(message, ":fetdoge:375987462553731073")
            await bot.add_reaction(message, ":pat:290789859663282176")
            await bot.add_reaction(message, ":nut:348350754974728193")
            await bot.add_reaction(message, ":hand:348350777661587466")
        else:
            await bot.add_reaction(message, "\u2764")

async def edit(message):
    if not message.author.bot:
        await log.message(message, "edited")

async def deleted(message):
    await log.message(message, "deleted")

SAVEPIC = False

async def new_pic(bot, message):
    if message.author.id == constants.NYAid:
        return
    for pic in message.attachments:
        if SAVEPIC:
            url = pic["url"]
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            i = 0

            if url.split(".")[len(url.split("."))-1] == "gif":
                ext = "gif"
            else:
                ext = "png"
            while os.path.isfile("./pics/{}{}.{}".format(''.join(e for e in message.author.name if e.isalnum()), i, ext)):
                i+=1
            img.save("./pics/{}{}.{}".format(''.join(e for e in message.author.name if e.isalnum()), i, ext), save_all=1)
            await log.message(message, "pic", i)
        else:
            text = "{} | {} | {} | {} | {} \n".format(datetime.datetime.utcnow(), message.server.name, message.channel.name, message.author.name, pic["url"])
            file = open("logs/pics.txt","a+")
            file.write(text)
            file.close
            print(text)