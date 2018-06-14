import datetime,  discord, unicodedata, constants


def str_cmd(s: str):
    return s.encode("ascii", "replace").decode("ascii")


async def error(event, filename="errors"):
    text = datetime.datetime.utcnow().strftime("%H:%M:%S") + " | " + str_cmd(event)
    file = open("logs/" + str_cmd(filename.replace('/', '')) + ".txt", "a+")
    file.write(text + '\n')
    file.close()
    print(text)


async def message(mess: discord.Message, action: str, number=0):
    file = open("logs/" + str_cmd(mess.server.name.replace('/', '')) + ".txt", "a+")
    if action == "pic":
        text = "{} | {} | {} posted a pic: {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(mess.channel.name), str_cmd(mess.author.name), number)
    else:
        members = list(map(mess.server.get_member, mess.raw_mentions))
        cont = mess.content
        for user in members:
            cont = cont.replace(user.mention, "@" + user.name)
        text = "{} | {} | {} | {} | {} : {}".format(mess.timestamp.strftime("%H:%M:%S"), mess.server.name.encode("ascii", "replace").decode("ascii"), str_cmd(mess.channel.name), str_cmd(mess.author.name), action, str_cmd(cont))
    file.write(text + "\n")
    print(text)
    file.close()
