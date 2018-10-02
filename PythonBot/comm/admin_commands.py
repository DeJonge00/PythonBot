import importlib
from random import randint

from discord.ext import commands
import comm, rpggame, musicPlayer

import constants


# Mod commands
class Admin:
    def __init__(self, my_bot):
        self.bot = my_bot
        print('Admin started')

    # {prefix}dm <user>|<message>
    @commands.command(pass_context=1, hidden=True)
    async def dm(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='dm', is_typing=False):
            return
        if not (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]):
            await self.bot.say("Hahahaha, no")
            return
        try:
            username, message = ' '.join(args).split('|')
        except ValueError:
            await self.bot.say('Not the right arguments, sweety')
            return
        try:
            user = await self.bot.get_member_from_message(ctx.message, args=username.split(' '), in_text=True,
                                                          from_all_members=True)
        except ValueError:
            return
        await self.bot.send_message(user, message)
        await self.bot.say('Message send to "{}"'.format(str(user)))

    # {prefix}emojispam <user>
    @commands.command(pass_context=1, hidden=True, help="Add a user to the emojispam list")
    async def emojispam(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='emojispam', is_typing=False):
            return
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
        if not await self.bot.pre_command(message=ctx.message, command='farecho', is_typing=False):
            return
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
            print('Response to farecho ({}, {}, {}): {}'.format(
                msg.author.name.encode("ascii", "replace").decode("ascii"),
                server_name.encode("ascii", "replace").decode("ascii"),
                channel_name.encode("ascii", "replace").decode("ascii"),
                msg.content.encode("ascii", "replace").decode("ascii")))

    # {prefix}getServerList
    @commands.command(pass_context=1, hidden=1, help="getServerList")
    async def getserverlist(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='getserverlist'):
            return
        if not (ctx.message.author.id == constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        m = ""
        for i in sorted([x for x in self.bot.servers], key=lambda l: len(l.members), reverse=True):
            m += "{}, members={}, owner={}\n".format(i.name, sum([1 for _ in i.members]), i.owner)
        # await self.bot.send_message(ctx.message.channel, m)
        print(m)

    # {prefix}reload <module>
    @commands.command(pass_context=1, hidden=True)
    async def reload(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='spam'):
            return
        if not (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]):
            await self.bot.say("Hahahaha, no")
            return

        self.load_cogs(self.bot, ' '.join(args))

    # {prefix}spam <amount> <user>
    @commands.command(pass_context=1, hidden=True, help="Spam a user messages")
    async def spam(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='spam'):
            return
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
    async def spongespam(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='spongespam'):
            return
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

    # {prefix}quit
    @commands.command(pass_context=1, hidden=True, help="Lets me go to sleep")
    async def quit(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='quit'):
            return
        if not ((ctx.message.author.id == constants.NYAid) | (ctx.message.author.id == constants.KAPPAid)):
            await self.bot.say("Hahahaha, no")
            return
        await self.bot.send_message(ctx.message.channel, "ZZZzzz...")
        await self.quitBot()

    @staticmethod
    def load_cogs(bot, cog: str):
        if cog in ['basics', 'all']:
            bot.remove_cog('Basics')
            importlib.reload(comm.basic_commands)
            from comm.basic_commands import Basics
            bot.add_cog(Basics(bot))

        if cog in ['minesweeper', 'ms', 'all']:
            bot.remove_cog('Minesweeper')
            importlib.reload(comm.minesweeper)
            from comm.minesweeper import Minesweeper
            bot.add_cog(Minesweeper(bot))

        if cog in ['hangman', 'all']:
            bot.remove_cog('Hangman')
            importlib.reload(comm.hangman)
            from comm.hangman import Hangman
            bot.add_cog(Hangman(bot))

        if cog in ['image', 'images', 'all']:
            bot.remove_cog('Images')
            importlib.reload(comm.image_commands)
            from comm.image_commands import Images
            bot.add_cog(Images(bot))

        if cog in ['lookup', 'all']:
            bot.remove_cog('Lookup')
            importlib.reload(comm.lookup_commands)
            from comm.lookup_commands import Lookup
            bot.add_cog(Lookup(bot))

        if bot.MUSIC and cog in ['music', 'all']:
            bot.remove_cog('MusicPlayer')
            importlib.reload(musicPlayer)
            from musicPlayer import MusicPlayer
            bot.musicplayer = MusicPlayer(bot)
            bot.add_cog(bot.musicplayer)

        if bot.RPGGAME and cog in ['rpg', 'all']:
            bot.remove_cog('RPGGame')
            bot.remove_cog('RPGGameActivities')
            importlib.reload(rpggame.rpgmain)
            importlib.reload(rpggame.rpggameactivities)
            from rpggame.rpgmain import RPGGame
            from rpggame.rpggameactivities import RPGGameActivities
            bot.rpggame = RPGGame(bot)
            bot.rpgshop = RPGGameActivities(bot)
            bot.add_cog(bot.rpggame)
            bot.add_cog(bot.rpgshop)

        if cog in ['mod', 'all']:
            bot.remove_cog('Mod')
            importlib.reload(comm.mod_commands)
            from comm.mod_commands import Mod
            bot.add_cog(Mod(bot))

        if cog in ['config', 'all']:
            bot.remove_cog('Config')
            importlib.reload(comm.config_commands)
            from comm.config_commands import Config
            bot.add_cog(Config(bot))

        if cog in ['misc', 'all']:
            bot.remove_cog('Misc')
            importlib.reload(comm.misc_commands)
            from comm.misc_commands import Misc
            bot.add_cog(Misc(bot))
