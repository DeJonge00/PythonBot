import asyncio, discord, constants, log
from discord.ext import commands
from random import randint

# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    # {prefix}banish <@person>
    @commands.command(pass_context=1, hidden=1, help="BANHAMMER")
    async def banish(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            for user in ctx.message.mentions:
                self.bot.kick(user)
        except Exception as e:
            await log.error("cmd banish: " + str(e))

    # {prefix}purge <amount>
    @commands.command(pass_context=1, hidden=1, help="Lets me go to sleep")
    async def purge(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            if len(args) > 0:
                try:
                    l = int(args[0])
                except ValueError:
                    l = 10
            else:
                l = 10
            await self.bot.purge_from(ctx.message.channel, limit=l)
        except Exception as e:
            await log.error("cmd purge: " + str(e))

    # {prefix}emojispam <user>
    @commands.command(pass_context=1, hidden=1, help="Add a user to the emojispam list")
    async def emojispam(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            if len(ctx.message.mentions) > 0:
                if ctx.message.mentions[0].id in self.bot.spamlist:
                    self.bot.spamlist.remove(ctx.message.mentions[0].id)
                else:
                    self.bot.spamlist.append(ctx.message.mentions[0].id)
        except Exception as e:
            await log.error("cmd emojispam: " + str(e))

    # {prefix}nickname <@person>
    @commands.command(pass_context=1, hidden=1, help="Nickname a person", aliases=["nick", "nn"])
    async def nickname(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            if len(ctx.message.mentions) > 0:
                if len(args) > 1:
                    await self.bot.change_nickname(ctx.message.mentions[0], " ".join(args[1:]))
                else:
                    await self.bot.change_nickname(ctx.message.mentions[0], "")
        except Exception as e:
            await log.error("cmd nickname: " + str(e))

    # {prefix}spam <amount> <user>
    @commands.command(pass_context=1, hidden=1, help="Spam a user messages")
    async def spam(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            if len(ctx.message.mentions) > 0:
                user = ctx.message.mentions[0]
                if len(args) > 1:
                    try:
                        a = int(args[0])
                    except ValueError:
                        a = 1
                    for i in range(a):
                        await self.bot.send_message(user, "Have a random number: " + str(randint(0,10000)) + " :heart:")
        except Exception as e:
            await log.error("cmd spam: " + str(e))

    # {prefix}quit
    @commands.command(pass_context=1, hidden=1, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            await self.bot.send_message(ctx.message.channel, "ZZZzzz...")
            await self.bot.rpggameinstance.quit()
            asyncio.sleep(3)
            await self.bot.logout()
            await self.bot.close()
        except Exception as e:
            await log.error("cmd quit: " + str(e))

    # Test command
    @commands.command(pass_context=1, hidden=1, help="test")
    async def test(self, ctx, *args):
        await self.bot.send_message(ctx.message.channel, "<:nya:256403423916720128>")
        await self.bot.add_reaction(ctx.message, ":nya:256403423916720128")