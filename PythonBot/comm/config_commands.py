import discord
from discord.ext import commands
import constants


class Config:
    def __init__(self, my_bot: discord.Client):
        self.bot = my_bot
        self.patTimes = {}

    # {prefix}botstats
    @commands.command(pass_context=1, help="Toggle whether commands will be deleted in the current server", aliases=['tdc'])
    async def toggledeletecommands(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='botstats'):
            return
        perms: discord.Permissions
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not ((ctx.message.author.id == constants.NYAid) or (perms.administrator)):
            await self.bot.say("Hahahaha, no")
            return

        self.bot.dont_delete_commands_servers: list
        if ctx.message.server.id in self.bot.dont_delete_commands_servers:
            self.bot.dont_delete_commands_servers.remove(ctx.message.server.id)
            await self.bot.say('Commands will now be deleted in this server')
        else:
            self.bot.dont_delete_commands_servers.append(ctx.message.server.id)
            await self.bot.say('Commands will now not be deleted in this server')
