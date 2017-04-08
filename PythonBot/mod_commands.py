import discord, log
from discord.ext import commands
import constants

# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    @commands.command(pass_context=1, hidden=1, help="Lets me go to sleep")
    async def purge(self, ctx, *args):
        try:
            try:
                self.bot.delete_message(ctx.message)
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

    @commands.command(pass_context=1, hidden=1, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        try:
            try:
                self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
            if ctx.message.author.id != constants.NYAid:
                return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
            await self.bot.logout()
            await self.bot.close()
        except Exception as e:
            await log.error("cmd quit: " + str(e))