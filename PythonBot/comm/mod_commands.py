import asyncio, discord, constants, log, pickle
from discord.ext import commands
from random import randint

# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    # {prefix}banish <@person>
    @commands.command(pass_context=1, help="BANHAMMER")
    async def banish(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        for user in ctx.message.mentions:
            await self.bot.kick(user)

    # {prefix}purge <amount>
    @commands.command(pass_context=1, help="Lets me go to sleep")
    async def purge(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        if len(args) > 0:
            try:
                l = int(args[0])
            except ValueError:
                l = 10
        else:
            l = 10
        await self.bot.purge_from(ctx.message.channel, limit=l)

    # {prefix}emojispam <user>
    @commands.command(pass_context=1, help="Add a user to the emojispam list")
    async def emojispam(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spamlist:
                self.bot.spamlist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spamlist.append(ctx.message.mentions[0].id)

    # {prefix}getServerList 
    @commands.command(pass_context=1, hidden=1, help="getServerList")
    async def getServerList(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        m = "";
        for i in self.bot.servers:
            m += i.name + "\n";
        return await self.bot.send_message(ctx.message.channel, m)

    # {prefix}nickname <@person>
    @commands.command(pass_context=1, help="Nickname a person", aliases=["nick", "nn"])
    async def nickname(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        if len(ctx.message.mentions) > 0:
            if len(args) > 1:
                await self.bot.change_nickname(ctx.message.mentions[0], " ".join(args[1:]))
            else:
                await self.bot.change_nickname(ctx.message.mentions[0], "")

    # {prefix}setgoodbye <message>
    @commands.command(pass_context=1, help="Sets a goodbye message")
    async def setgoodbye(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        self.bot.goodbye[ctx.message.server.id] = " ".join(args)

    # {prefix}setwelcome <message>
    @commands.command(pass_context=1, help="Sets a welcome message")
    async def setwelcome(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        self.bot.welcome[ctx.message.server.id] = " ".join(args)

    # {prefix}spam <amount> <user>
    @commands.command(pass_context=1, help="Spam a user messages")
    async def spam(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0]
            if len(args) > 1:
                try:
                    a = int(args[0])
                except ValueError:
                    a = 1
                for i in range(a):
                    await self.bot.send_message(user, "Have a random number: " + str(randint(0,10000)) + " :heart:")

    # {prefix}spongespam <user>
    @commands.command(pass_context=1, help="Add a user to the spongespam list")
    async def spongespam(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        if len(ctx.message.mentions) > 0:
            if ctx.message.mentions[0].id in self.bot.spongelist:
                self.bot.spongelist.remove(ctx.message.mentions[0].id)
            else:
                self.bot.spongelist.append(ctx.message.mentions[0].id)

    # {prefix}quit
    @commands.command(pass_context=1, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        await self.deleteAndCheck(ctx);
        await self.bot.send_message(ctx.message.channel, "ZZZzzz...")
        await self.bot.rpggameinstance.quit()
        with open(self.bot.WELCOMEMESSAGEFILE, 'wb') as fp:
            pickle.dump(self.bot.welcome, fp)
        with open(self.bot.GOODBYEMESSAGEFILE, 'wb') as fp:
            pickle.dump(self.bot.goodbye, fp)
        asyncio.sleep(3)
        await self.bot.logout()
        await self.bot.close()

    # Test command
    @commands.command(pass_context=1, hidden=1, help="test")
    async def test(self, ctx, *args):    
        emoji = args[0].split(':', 1)[-1].split(':', 1)[0]  
        emojis = self.bot.get_all_emojis();
        for e in emojis:
            if(e.name == emoji):
                return await self.bot.send_message(ctx.message.channel, url(e))
                

    async def deleteAndCheck(self, ctx):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        if ctx.message.author.id != constants.NYAid:
            return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")