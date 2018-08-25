import discord
from discord.ext import commands
import constants


class Config:
    def __init__(self, my_bot: discord.Client):
        self.bot = my_bot
        self.patTimes = {}

    # {prefix}botstats
    @commands.command(pass_context=1, help="Toggle whether commands will be deleted here",
                      aliases=['tdc'])
    async def toggledeletecommands(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='toggledeletecommands', cannot_be_private=True):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not ((ctx.message.author.id == constants.NYAid) or (perms.manage_messages)):
            await self.bot.say("Hahahaha, no")
            return

        if ctx.message.server.id in self.bot.dont_delete_commands_servers:
            self.bot.dont_delete_commands_servers.remove(ctx.message.server.id)
            await self.bot.say('Commands will now be deleted in this server')
        else:
            self.bot.dont_delete_commands_servers.append(ctx.message.server.id)
            await self.bot.say('Commands will now not be deleted in this server')

    @commands.command(pass_context=1, help="Toggle whether a specific commands can be used here", aliases=['tc'])
    async def togglecommand(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='togglecommand', cannot_be_private=True):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_channels or perms.administrator):
            await self.bot.say("Hahahaha, no")
            return
        if len(args) <= 1 or args[0] not in ['server', 'channel']:
            await self.bot.say('Please give me either "server" or "channel" followed by the name of the command')
            return

        # Find if comand exists and convert possible aliases
        comm = self.bot
        try:
            for name in args[1:]:
                comm = comm.commands.get(name)
        except AttributeError:
            await self.bot.say('I do not recognize that command name. Maybe you used an alias?')
            return
        name = comm.name

        # Lookup spot in the bot commands_banned_in dictionary
        if not self.bot.commands_banned_in.get(args[0]):
            self.bot.commands_banned_in[args[0]] = {}
        cs = self.bot.commands_banned_in.get(args[0])
        identifier = ctx.message.server.id if args[0] == 'server' else ctx.message.channel.id
        if not cs.get(identifier):
            cs[identifier] = []
        cs = cs.get(identifier)

        # Add or remove command
        if name == 'togglecommand':
            await self.bot.say('Wow... just wow')
            return
        if name in cs:
            cs.remove(name)
            await self.bot.say('Command "{}" is now unbanned from this {}'.format(name, args[0]))
        else:
            cs.append(name)
            await self.bot.say('Command "{}" is now banned from this {}'.format(name, args[0]))
