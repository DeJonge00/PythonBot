import asyncio, discord, constants, log, pickle, removeMessage, sqlite3
from discord.ext import commands
from random import randint

# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    # {prefix}banish <@person>
    @commands.command(pass_context=1, help="BANHAMMER")
    async def banish(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not((ctx.message.author.id==constants.NYAid) | (perms.kick_members)):
            await self.bot.say("Hahahaha, no")
            return
        for user in ctx.message.mentions:
            await self.bot.kick(user)
    
    #{prefix}reset
    @commands.group(pass_context=1, help="'>help reset' for full options")
    async def reset(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # {prefix}emojispam <user>
    @commands.command(pass_context=1, help="Add a user to the emojispam list")
    async def emojispam(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spamlist:
                self.bot.spamlist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spamlist.append(ctx.message.mentions[0].id)

    # {prefix}getServerList 
    @commands.command(pass_context=1, hidden=1, help="getServerList")
    async def getServerList(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        m = "";
        for i in self.bot.servers:
            m += i.name + "\n";
        await self.bot.send_message(ctx.message.channel, m)

    # {prefix}nickname <@person>
    @commands.command(pass_context=1, help="Nickname a person", aliases=["nick", "nn"])
    async def nickname(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if len(ctx.message.mentions) > 0:
            if len(args) > 1:
                if not((ctx.message.author.id==constants.NYAid) | (perms.manage_nicknames)):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], " ".join(args[1:]))
            else:
                if not((ctx.message.author.id==constants.NYAid) | (perms.change_nickname)):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], "")

    # {prefix}reset pats
    @reset.command(pass_context=1, help="Reset pat db")
    async def pats(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
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
        await removeMessage.deleteMessage(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not((ctx.message.author.id==constants.NYAid) | (perms.manage_messages)):
            await self.bot.say("Hahahaha, no")
            return
        if len(args) > 0:
            try:
                l = int(args[0])
            except ValueError:
                l = 10
        else:
            l = 10
        if len(ctx.message.mentions)>0:
            def c(message):
                return message.author in ctx.message.mentions
            return await self.bot.purge_from(ctx.message.channel, check=c, limit=l)
        await self.bot.purge_from(ctx.message.channel, limit=l)

    # {prefix}resetgoodbye
    @reset.command(pass_context=1, help="Resets all goodbye messages")
    async def goodbye(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
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
        await removeMessage.deleteMessage(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not((ctx.message.author.id==constants.NYAid) | (perms.manage_server)):
            await self.bot.say("Hahahaha, no")
            return
        conn = sqlite3.connect(constants.GOODBYEMESSAGEFILE)
        c = conn.cursor()
        c.execute("SELECT * FROM goodbye WHERE serverID=" + ctx.message.server.id)
        r = c.fetchone()
        if r == None:
            c.execute("INSERT INTO goodbye VALUES ('" + ctx.message.server.id + "', '" + " ".join(args) + "')")
        else:
            c.execute("UPDATE goodbye SET message='"+ " ".join(args) +"' WHERE serverID=" + ctx.message.server.id)
        conn.commit()
        conn.close()
        await self.bot.say("Goodbye message for this server is now: " + " ".join(args).format("<user mention>"))

    # {prefix}resetwelcome
    @reset.command(pass_context=1, help="Resets all welcome messages")
    async def welcome(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
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
        await removeMessage.deleteMessage(self.bot, ctx)
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not((ctx.message.author.id==constants.NYAid) | (perms.manage_server)):
            await self.bot.say("Hahahaha, no")
            return
        conn = sqlite3.connect(constants.WELCOMEMESSAGEFILE)
        c = conn.cursor()
        c.execute("SELECT * FROM welcome WHERE serverID=" + ctx.message.server.id)
        r = c.fetchone()
        if r == None:
            c.execute("INSERT INTO welcome VALUES ('" + ctx.message.server.id + "', '" + " ".join(args) + "')")
        else:
            c.execute("UPDATE welcome SET message='"+ " ".join(args) +"' WHERE serverID=" + ctx.message.server.id)
        conn.commit()
        conn.close()
        await self.bot.say("Welcome message for this server is now: " + " ".join(args).format("<user mention>"))

    # {prefix}spam <amount> <user>
    @commands.command(pass_context=1, help="Spam a user messages")
    async def spam(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
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
                    await self.bot.send_message(user, "Have a random number: " + str(randint(0,10000)) + " :heart:")

    # {prefix}spongespam <user>
    @commands.command(pass_context=1, help="Add a user to the spongespam list")
    async def spongespam(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spongelist:
                self.bot.spongelist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spongelist.append(ctx.message.mentions[0].id)

    async def quitBot(self):
        try:
            if self.bot.RPGGAME:
                await self.bot.rpggame.quit()
            if self.bot.MUSIC:
                if self.bot.musicplayer != None:
                    self.bot.musicplayer.quit()
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
    @commands.command(pass_context=1, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        await self.bot.send_message(ctx.message.channel, "ZZZzzz...")
        await self.quitBot()
        

    # Test command
    @commands.command(pass_context=1, hidden=1, help="test")
    async def test(self, ctx, *args):    
        #await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        await self.bot.rpggameinstance.bossbattle()