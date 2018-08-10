from discord.ext import commands
from discord.ext.commands import Bot
import asyncio, removeMessage

class Misc:
    def __init__(self, my_bot):
        self.bot = my_bot

    @commands.command(pass_context=1, help="Invite me to your own server")
    async def inviteme(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        await self.bot.say("Here is a link to invite me:\nhttps://discordapp.com/api/oauth2/authorize?client_id=244410964693221377&scope=bot&permissions=0")

    @commands.command(pass_context=1, help="Join my masters discord server if questions need answering")
    async def helpserver(self, ctx, *args):
        await removeMessage.delete_message(self.bot, ctx)
        await self.bot.say("A link to the past:\nhttps://discord.gg/KBxRd7x")