import asyncio, discord, constants, log, pickle, removeMessage, sqlite3, os, requests, dbconnect, re
from discord.ext import commands
from random import randint
from PIL import Image
from io import BytesIO
from datetime import datetime


# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    # {prefix}banish <@person>
    @commands.command(pass_context=1, help="BANHAMMER")
    async def banish(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not ((ctx.message.author.id == constants.NYAid) | (perms.kick_members)):
            await self.bot.say("Hahahaha, no")
            return
        for user in ctx.message.mentions:
            await self.bot.kick(user)

    # {prefix}reset
    @commands.group(pass_context=1, hidden=True, help="'>help reset' for full options")
    async def reset(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # {prefix}emojispam <user>
    @commands.command(pass_context=1, hidden=True, help="Add a user to the emojispam list")
    async def emojispam(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx, istyping=False)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spamlist:
                self.bot.spamlist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spamlist.append(ctx.message.mentions[0].id)

    # {prefix}farecho <server>|<channel>|<words>
    @commands.command(pass_context=1, hidden=True, help="I'll be a parrot!")
    async def farecho(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx, istyping=False)
        if not (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]):
            await self.bot.say("Hahahaha, no")
            return
        try:
            server_name, channel_name, message = ' '.join(args).split('|')
            server_name = server_name.lower()
            channel_name = channel_name.lower()
        except ValueError:
            await self.bot.say('Not the right arguments, sweety')
            return
        server = None
        channel = None
        for s in self.bot.servers:
            if s.name.lower().encode("ascii", "replace").decode("ascii") == server_name:
                server = s
                break
        if not server:
            await self.bot.say('Server not found')
            return

        for c in server.channels:
            if c.name.lower().encode("ascii", "replace").decode("ascii") == channel_name:
                channel = c
                break
        if not channel:
            await self.bot.say('Channel not found')
            return

        await self.bot.send_message(channel, message)

        for i in range(3):
            msg = await self.bot.wait_for_message(timeout=180, channel=channel)
            if not msg:
                return
            print('Response to farecho ({}, {}, {}): {}'.format(msg.author.encode("ascii", "replace").decode("ascii"),
                                                                server_name.encode("ascii", "replace").decode("ascii"),
                                                                channel_name.encode("ascii", "replace").decode("ascii"),
                                                                msg.content.encode("ascii", "replace").decode("ascii")))

    # {prefix}getServerList 
    @commands.command(pass_context=1, hidden=1, help="getServerList")
    async def getserverlist(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        m = ""
        for i in self.bot.servers:
            m += "{}, members={}, owner={}\n".format(i.name, sum([1 for _ in i.members]), i.owner)
        # await self.bot.send_message(ctx.message.channel, m)
        print(m)

    # {prefix}newpp <attach new pp>
    @commands.command(pass_context=1, help="Nickname a person")
    async def newpp(self, ctx, *args):
        if not (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].get('url')
        elif len(ctx.message.mentions) > 0:
            url = '.'.join(ctx.message.mentions[0].avatar_url.split('.')[:-1]) + '.png'
            print(url)
        else:
            await self.bot.say('Pls give me smth...')
            return
        try:
            # TODO: Fix saving pic first
            name = 'temp/newpp.png'
            Image.open(BytesIO(requests.get(url).content)).save(name)
            await removeMessage.delete_message(self.bot, ctx)
            with open(name, 'rb') as file:
                await self.bot.edit_profile(avatar=file.read())
            await self.bot.say('Make-up is done sweety <3')
        except requests.exceptions.MissingSchema:
            await self.bot.say('Thats not a valid target')
        except OSError:
            await self.bot.say('Thats not a valid target')
        except discord.HTTPException:
            await self.bot.say('Discord pls')
        finally:
            try:
                os.remove(name)
            except:
                pass

    # {prefix}nickname <@person>
    @commands.command(pass_context=1, help="Nickname a person", aliases=["nick", "nn"])
    async def nickname(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if len(ctx.message.mentions) > 0:
            if len(args) > 1:
                if not ((ctx.message.author.id == constants.NYAid) | (perms.manage_nicknames)):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], " ".join(args[1:]))
            else:
                if not ((ctx.message.author.id == constants.NYAid) | (perms.change_nickname)):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], "")

    # {prefix}reset pats
    @reset.command(pass_context=1, hidden=True, help="Reset pat db")
    async def pats(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        conn = sqlite3.connect(constants.PATSDB)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS author")
        c.execute("DROP TABLE IF EXISTS pats")
        c.execute("CREATE TABLE author (authorID INTEGER, time INTEGER)")
        c.execute("CREATE TABLE pats (authorID INTEGER, userID INTEGER, pats INTEGER)")
        conn.commit()
        conn.close()
        await self.bot.say("Pats reset")

    # {prefix}purge <amount>
    @commands.command(pass_context=1, help="Remove a weird chat")
    async def purge(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx, istyping=False)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not ((ctx.message.author.id == constants.NYAid) | (perms.manage_messages)):
            await self.bot.say("Hahahaha, no")
            return
        if len(args) > 0:
            try:
                l = int(args[0])
            except ValueError:
                l = 10
        else:
            l = 10
        if len(ctx.message.mentions) > 0:
            def c(message):
                return message.author in ctx.message.mentions

            return await self.bot.purge_from(ctx.message.channel, check=c, limit=l)
        await self.bot.purge_from(ctx.message.channel, limit=l)

    # {prefix}resetgoodbye
    @reset.command(pass_context=1, hidden=True, help="Resets all goodbye messages")
    async def goodbye(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        conn = sqlite3.connect(constants.GOODBYEMESSAGEFILE)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS goodbye")
        c.execute("CREATE TABLE goodbye (serverID INTEGER, message TEXT)")
        conn.commit()
        conn.close()
        await self.bot.say("Goodbye table reset")

    # {prefix}setgoodbye <message>
    @commands.command(pass_context=1, help="Sets a goodbye message")
    async def setgoodbye(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_server):
            await self.bot.say("Hahahaha, no")
            return
        if len(" ".join(args)) > 120:
            await self.bot.say("Sorry, this message is too long...")
            return
        if re.match('.*{.+}.*', " ".join(args)):
            await self.bot.say("Something went terribly wrong...")
            return
        dbconnect.set_message('on_member_remove', ctx.message.server.id, ctx.message.channel.id, " ".join(args))
        if len(args) > 0:
            await self.bot.say("Goodbye message for this server is now: " + " ".join(args).format("<user mention>"))
            return
        await self.bot.say("Goodbye message for this server has been reset")

    # {prefix}resetwelcome
    @reset.command(pass_context=1, hidden=True, help="Resets all welcome messages")
    async def welcome(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        conn = sqlite3.connect(constants.WELCOMEMESSAGEFILE)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS welcome")
        c.execute("CREATE TABLE welcome (serverID INTEGER, message TEXT)")
        conn.commit()
        conn.close()
        await self.bot.say("Welcome table reset")

    # {prefix}setwelcome <message>
    @commands.command(pass_context=1, help="Sets a welcome message")
    async def setwelcome(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_server):
            await self.bot.say("Hahahaha, no")
            return
        if len(" ".join(args)) > 120:
            await self.bot.say("Sorry, this message is too long...")
            return
        if re.match('.*{.+}.*', " ".join(args)):
            await self.bot.say("Something went terribly wrong...")
            return
        dbconnect.set_message('on_member_join', ctx.message.server.id, ctx.message.channel.id, " ".join(args))
        if len(args) > 0:
            await self.bot.say("Welcome message for this server is now: " + " ".join(args).format("<user mention>"))
            return
        await self.bot.say("Welcome message for this server has been reset")

    # {prefix}spam <amount> <user>
    @commands.command(pass_context=1, hidden=True, help="Spam a user messages")
    async def spam(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0]
            if len(args) > 1:
                try:
                    a = int(args[0])
                except ValueError:
                    a = 10
                for i in range(a):
                    await self.bot.send_message(user, "Have a random number: " + str(randint(0, 10000)) + " :heart:")

    # {prefix}spongespam <user>
    @commands.command(pass_context=1, hidden=True, help="Add a user to the spongespam list")
    async def spongespam(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spongelist:
                self.bot.spongelist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spongelist.append(ctx.message.mentions[0].id)

    async def quitBot(self):
        try:
            await self.bot.quit()
        except Exception as e:
            print(e)
        await self.bot.logout()
        await self.bot.close()

    #    # {prefix}restart
    #    @commands.command(pass_context=1, help="Lets me go to sleep AND BE RESURRECTED \\o/")
    #    async def restart(self, ctx, *args):
    #        await removeMessage.deleteMessage(self.bot, ctx)
    #        if not(ctx.message.author.id==constants.NYAid):
    #            await self.bot.say("Hahahaha, no")
    #            return
    #        await self.bot.send_message(ctx.message.channel, "*I'll be back...*")
    #
    #        reload(PythonBot)

    # {prefix}quit
    @commands.command(pass_context=1, hidden=True, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        if not ((ctx.message.author.id == constants.NYAid) | (ctx.message.author.id == constants.KAPPAid)):
            await self.bot.say("Hahahaha, no")
            return
        await self.bot.send_message(ctx.message.channel, "ZZZzzz...")
        await self.quitBot()

    # Test command
    @commands.command(pass_context=1, hidden=1, help="test")
    async def test(self, ctx, *args):
        # await removeMessage.deleteMessage(self.bot, ctx)
        if not (ctx.message.author.id == constants.NYAid or ctx.message.author.id == constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        import copydb
        time = datetime.now()
        print(time.isoformat())
        copydb.get_all_players()
        print((time - datetime.now()).seconds)
