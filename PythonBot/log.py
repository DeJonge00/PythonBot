import datetime,  discord, unicodedata

async def error(event, filename="errors"):
    file = open("logs/" + filename + ".txt","a+")
    file.write(str(datetime.datetime.utcnow()) + " | " + event.encode("ascii", "replace").decode("ascii") + "\n")
    file.close
    print(datetime.datetime.utcnow().strftime("%H:%M:%S") + " | " + event)

async def message(message : discord.Message, action : str, number=0):
    file = open("logs/" + message.server.name + ".txt","a+")
    if action == "pic":
        file.write(str(message.timestamp) + " | " + message.channel.name.encode("ascii", "replace").decode("ascii") + " | " + message.author.name.encode("ascii", "replace").decode("ascii") + " posted a pic, saved as " + str(number) + "\n")
        print(str(message.timestamp) + " | " + message.server.name + " | " + message.channel.name + " | " + message.author.name + " posted a pic, saved as " + str(number))
    else:
        members = list(map(message.server.get_member, message.raw_mentions))
        cont = message.content
        for user in members:
            cont = cont.replace(user.mention, "@" + user.name)
        file.write(str(message.timestamp) + " | " + message.channel.name.encode("ascii", "replace").decode("ascii") + " | " + message.author.name.encode("ascii", "replace").decode("ascii") + " " + action + ": " + cont.encode("ascii", "replace").decode("ascii") + "\n")
        print(str(message.timestamp) + " | " + message.server.name + " | " + message.channel.name + " | " + message.author.name + " " + action + ": " + cont)
    file.close