import datetime
import discord
import constants


def str_cmd(s: str):
    return s.encode("ascii", "replace").decode("ascii")


async def error(event, filename="errors", serverid=None):
    if serverid in constants.bot_list_servers:
        return
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
    if (not mess.channel.is_private) and mess.server.id in constants.bot_list_servers:
        return
    if mess.channel.is_private:
        servername = 'direct message'
        channelname = '-'
    else:
        servername = mess.server.name
        channelname = mess.channel.name
    file = open("logs/" + str_cmd(servername.replace('/', '')) + ".txt", "a+")
    if action == "pic":
        text = "{} | {} | {} | {} posted a pic: {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(servername), str_cmd(channelname), str_cmd(str(mess.author)), number)
    else:
        cont = mess.content
        if not mess.channel.is_private:
            members = list(map(mess.server.get_member, mess.raw_mentions))
            for user in members:
                try:
                    cont = cont.replace(user.mention, "@" + user.name)
                except AttributeError:
                    pass
        text = "{} | {} | {} | {} | {} : {}".format(mess.timestamp.strftime("%H:%M:%S"), str_cmd(servername), str_cmd(channelname), str_cmd(str(mess.author)), action, str_cmd(cont))
    file.write(text + "\n")
    print(text)
    file.close()
