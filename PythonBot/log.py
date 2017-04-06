import datetime
import discord

async def error(event, message=None):
    file = open("logs/errors.txt","a+")
    file.write(datetime.datetime.utcnow().strftime("%H:%M:%S") + " | error:" + event)
    file.close
    print(datetime.datetime.utcnow().strftime("%H:%M:%S") + " | error:" + event)

async def message(message, action, number=0):
    if not isinstance(message, discord.Message):
        print("Error in log.log: not a discord.Message")
        return;
    if not isinstance(action, str):
        print("Error in log.log: not a string")
        return;

    file = open("logs/" + message.server.name + ".txt","a+")
    if action == "pic":
        file.write(message.timestamp.strftime("%H:%M:%S") + " | " + message.channel.name + " | " + message.author.name + " posted a pic, saved as " + str(number) + "\n")
    else:
        file.write(message.timestamp.strftime("%H:%M:%S") + " | " + message.channel.name + " | " + message.author.name + " " + action + ": " + message.content + "\n")
        if len(message.mentions) >= 0:
            file.write(" ".join(message.mentions))
    file.close
    if action == "pic":
        print(message.timestamp.strftime("%H:%M:%S") + " | " + message.server.name + " | " + message.channel.name + " | " + message.author.name + " " + action + " posted a pic, saved as " + str(number))
    else:
        print(message.timestamp.strftime("%H:%M:%S") + " | " + message.server.name + " | " + message.channel.name + " | " + message.author.name + " " + action + ": " + message.content)
    if len(message.mentions) > 0:
        print(" ".join(message.mentions))