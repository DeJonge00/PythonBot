import datetime
import discord


def str_cmd(s: str):
    return s.encode("ascii", "replace").decode("ascii")


async def error(event, filename="errors"):
    text = datetime.datetime.utcnow().strftime("%H:%M:%S") + " | " + str_cmd(event)
    file = open("logs/" + str_cmd(filename.replace('/', '')) + ".txt", "a+")
    file.write(text + '\n')
    file.close()
    print(text)


async def log(note, author, string, filename):
    file = open("logs/" + str_cmd(filename.replace('/', '')) + ".txt", "a+")
    text = "{} | {} | {} : {}".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), str_cmd(note), str_cmd(author), str_cmd(string))
    file.write(text + "\n")
    print(text)


async def message(mess: discord.Message, action: str, number=0):
    file = open("logs/" + str_cmd(mess.server.name.replace('/', '')) + ".txt", "a+")
    if action == "pic":
        if mess.channel.is_private:
            text = "{} | direct message | {} | {} posted a pic: {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(mess.channel.name), str_cmd(mess.author.name), number)
        else:
            text = "{} | {} | {} | {} posted a pic: {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(mess.server.name), str_cmd(mess.channel.name), str_cmd(mess.author.name), number)
    else:
        members = list(map(mess.server.get_member, mess.raw_mentions))
        cont = mess.content
        for user in members:
            try:
                cont = cont.replace(user.mention, "@" + user.name)
            except AttributeError:
                pass
        text = "{} | {} | {} | {} | {} : {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(mess.server.name), str_cmd(mess.channel.name), str_cmd(mess.author.name), action, str_cmd(cont))
    file.write(text + "\n")
    print(text)
    file.close()
