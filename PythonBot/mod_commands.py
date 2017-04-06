import discord
from discord.ext import commands
import constants

# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot

    @commands.command(pass_context=1, hidden=1, help="Lets me go to sleep")
    async def quit(self, ctx, *args):
        if ctx.message.author.id != constants.NYAid:
            return await self.bot.send_message(ctx.message.channel, "Hahaha, no.")
