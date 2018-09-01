#!/usr/bin/env python3
import asyncio
import re

import discord

from discord.ext.commands import Bot

import constants
import customHelpFormatter
import datetime
import dbconnect
import log
import logging
import message_handler

from secret import secrets

# Basic configs
pi = 3.14159265358979323846264
REMOVE_JOIN_MESSAGE = False
REMOVE_LEAVE_MESSAGE = False


def initCogs(bot):
    # Add commands
    from comm.basic_commands import Basics
    bot.add_cog(Basics(bot))
    from comm.minesweeper import Minesweeper
    bot.add_cog(Minesweeper(bot))
    from comm.hangman import Hangman
    bot.add_cog(Hangman(bot))
    from comm.image_commands import Images
    bot.add_cog(Images(bot))
    if bot.MUSIC:
        from musicPlayer import MusicPlayer
        bot.musicplayer = MusicPlayer(bot)
        bot.add_cog(bot.musicplayer)
    if bot.RPGGAME:
        from rpggame.rpgmain import RPGGame
        from rpggame.rpgshop import RPGShop
        bot.rpggame = RPGGame(bot)
        bot.rpgshop = RPGShop(bot)
        bot.add_cog(bot.rpggame)
        bot.add_cog(bot.rpgshop)
    from comm.mod_commands import Mod
    bot.add_cog(Mod(bot))
    from comm.config_commands import Config
    bot.add_cog(Config(bot))
    from comm.misc_commands import Misc
    bot.add_cog(Misc(bot))


class PythonBot(Bot):
    def __init__(self, music=True, rpggame=True):
        self.praise = datetime.datetime.utcnow()

        self.spamlist = []
        self.spongelist = []

        # List of server ids (str)
        self.dont_delete_commands_servers = []

        # Dict of
        #    'server': Dict of 'serverid': ['command_name']
        # or 'channel': Dict of 'channelid': ['command_name']
        self.commands_banned_in = {}

        self.commands_counters = {}

        self.MUSIC = music
        self.RPGGAME = rpggame
        super(PythonBot, self).__init__(command_prefix=secrets.prefix, pm_help=1,
                                        formatter=customHelpFormatter.customHelpFormatter())

    @staticmethod
    def prep_str_for_print(s: str):
        return s.encode("ascii", "replace").decode("ascii")

    async def delete_command_message(self, message):
        try:
            if not message.channel.is_private:
                await self.delete_message(message)
        except (discord.Forbidden, discord.ext.commands.errors.CommandInvokeError):
            pass

    def command_allowed_in(self, type: str, command_name: str, identifier: str):
        return command_name == 'togglecommand' or not any(
            set([command_name, 'all']).intersection(set(self.commands_banned_in.get(type, {}).get(identifier, []))))

    def command_allowed_in_server(self, command_name: str, serverid: str):
        return self.command_allowed_in('server', command_name, serverid)

    def command_allowed_in_channel(self, command_name: str, channelid: str):
        return self.command_allowed_in('channel', command_name, channelid)

    async def pre_command(self, message: discord.Message, command: str, is_typing=True, delete_message=True,
                          cannot_be_private=False, must_be_private=False):

        if message.channel.is_private:
            if cannot_be_private:
                await self.send_message(message.channel, 'This command cannot be used in private channels')
                await log.message(message, 'Command "{}" used, but cannot be private'.format(command))
                return False
        else:
            if must_be_private:
                await self.send_message(message.channel, 'This command has to be used in a private conversation')
                await log.message(message, 'Command "{}" used, but must be private'.format(command))
                return False
            if not self.command_allowed_in_server(command, message.server.id):
                await log.message(message, 'Command "{}" used, but is serverbanned'.format(command))
                return False
            if not self.command_allowed_in_channel(command, message.channel.id):
                await log.message(message, 'Command "{}" used, but is channelbanned'.format(command))
                return False
            if delete_message and message.server.id not in self.dont_delete_commands_servers:
                await self.delete_command_message(message)

        await log.message(message, 'Command "{}" used'.format(command))
        if is_typing:
            await self.send_typing(message.channel)
        if self.commands_counters.get(command):
            self.commands_counters[command] += 1
        else:
            self.commands_counters[command] = 1
        return True

    @staticmethod
    def prep_str(s):
        new_s = ''
        for l in s:
            if re.match('[a-zA-Z0-9]', l):
                new_s += l
        return new_s

    # errors = {
    #   'no_mention': No user was mentioned in the message,
    #   'no_user': No user was found with the given name,
    #   'no_reaction': The user did not react to the choice within a minute
    # }
    async def get_member_from_message(self, message: discord.Message, args: list, in_text=False,
                                      errors: dict = {}, from_all_members=False) -> discord.Member:
        if len(message.mentions) > 0:
            return message.mentions[0]

        if len(args) <= 0 or (message.channel.is_private and not from_all_members):
            return message.author

        if not in_text:
            if errors:
                error = errors.get('no_mention') if errors.get('no_mention') else 'Please mention a user'
                await self.send_message(message.channel, error)
            raise ValueError

        name = PythonBot.prep_str(' '.join(args)).lower()
        if from_all_members:
            users = [x for x in self.get_all_members() if PythonBot.prep_str(x.name).lower().startswith(name) or
                     PythonBot.prep_str(x.display_name).lower().startswith(name)]
        else:
            users = [x for x in message.server.members if PythonBot.prep_str(x.name).lower().startswith(name) or
                     PythonBot.prep_str(x.display_name).lower().startswith(name)]
        users.sort(key=lambda s: len(s.name))

        if len(users) <= 0:
            if errors:
                error = errors.get('no_users') if errors.get('no_users') else 'I could not find a user with that name'
                await self.say(error)
            raise ValueError
        if len(users) == 1:
            return users[0]

        # Multiple users found, ask user which one he meant
        m = 'Which user did you mean?'
        for x in range(min(len(users), 10)):
            m += '\n{}) {}'.format(x + 1, str(users[x]))
        m = await self.say(m)
        r = await self.wait_for_message(timeout=60, author=message.author,
                                        channel=message.channel)

        if message.server.id not in self.dont_delete_commands_servers:
            await self.delete_message(m)
            if r:
                await self.delete_message(r)

        if not r:
            if errors:
                error = errors.get('no_reaction') if errors.get('no_reaction') else 'Or not...'
                await self.say(error)
            raise ValueError
        try:
            num = int(r.content) - 1
            if not (0 <= num < min(10, len(users))):
                raise ValueError
        except ValueError:
            await self.say('That was not a valid number')
            raise
        return users[num]

    async def timeLoop(self):
        await self.wait_until_ready()
        self.running = True
        while self.running:
            time = datetime.datetime.utcnow()

            if self.RPGGAME:
                await self.rpggame.game_tick(time)
            if self.MUSIC:
                await self.musicplayer.music_loop(time)

            endtime = datetime.datetime.utcnow()
            # print("Sleeping for " + str(60-(endtime).second) + "s")
            await asyncio.sleep(60 - endtime.second)

    async def quit(self):
        self.running = False
        for key in self.commands_counters.keys():
            print('Command "{}" was used {} times'.format(key, self.commands_counters.get(key)))
        dbconnect.set_do_not_delete_commands(self.dont_delete_commands_servers)
        dbconnect.set_banned_commands('server', self.commands_banned_in.get('server'))
        dbconnect.set_banned_commands('channel', self.commands_banned_in.get('channel'))
        if self.RPGGAME:
            self.rpggame.quit()
        if self.MUSIC:
            await self.musicplayer.quit()

    async def on_member_message(self, member, func_name, text) -> bool:
        await log.error(member.server.name + " | Member " + member.name + " just " + text, filename=member.server.name,
                        serverid=member.server.id)
        response = dbconnect.get_message(func_name, member.server.id)
        if not response:
            return False
        channel, mes = response
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="User {}!".format(self.prep_str_for_print(text)), value=mes.format(member.mention))
        channel = self.get_channel(channel)
        if not channel:
            print('CHANNEL NOT FOUND')
            return False
        m = await self.send_message(channel, embed=embed)
        if REMOVE_JOIN_MESSAGE:
            await asyncio.sleep(30)
            try:
                await self.delete_message(m)
            except discord.Forbidden:
                print(member.server + " | No permission to delete messages")
        return True


def init_bot():
    bot = PythonBot()
    logging.basicConfig()
    initCogs(bot)
    bot.dont_delete_commands_servers = dbconnect.get_do_not_delete_commands()
    bot.commands_banned_in['server'] = dbconnect.get_banned_commands('server')
    bot.commands_banned_in['channel'] = dbconnect.get_banned_commands('channel')
    bot.loop.create_task(bot.timeLoop())

    @bot.event
    async def on_ready():
        print('\nStarted bot')
        print("User: " + bot.user.name)
        print("Disc: " + bot.user.discriminator)
        print("ID: " + bot.user.id)
        print("Started at: " + datetime.datetime.utcnow().strftime("%H:%M:%S") + "\n")
        if not hasattr(bot, 'uptime'):
            bot.uptime = datetime.datetime.utcnow()
        await bot.change_presence(game=discord.Game(name='with lolis <3'), status=discord.Status.do_not_disturb)

    # Handle incoming events
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.channel.is_private:
            await log.log("direct message", message.author.name, message.content, "dm")
            for pic in message.attachments:
                await log.message(message, "pic", pic["url"])
        else:
            if (message.server.id == constants.NINECHATid) & (not message.server.get_member(constants.NYAid)):
                print(
                    message.server.name + "-" + message.channel.name + " (" + message.user.name + ") " + message.content)
            if message.content and message.server.id not in constants.bot_list_servers:
                await message_handler.new(bot, message)
        # Commands in the message
        try:
            await bot.process_commands(message)
        except discord.errors.Forbidden:
            await log.message(message, 'Forbidden Exception')
            pass
            await bot.send_message(message.channel, 'I\'m sorry, but my permissions do not allow that...')
        # Send message to rpggame for exp
        if bot.RPGGAME:
            await bot.rpggame.handle(message)

    # @bot.event
    # async def on_message_edit(before, after):
    #     await message_handler.edit(before)
    #
    # @bot.event
    # async def on_message_delete(message):
    #     await message_handler.deleted(message)

    @bot.event
    async def on_member_join(member: discord.Member):
        if member.bot:
            return
        await bot.on_member_message(member, "on_member_join", 'joined')

    @bot.event
    async def on_member_remove(member: discord.Member):
        if member.bot:
            return
        await bot.on_member_message(member, "on_member_remove", 'left')

    # @bot.event
    # async def on_voice_state_update(before, after):
    #     if bot.MUSIC:
    #         if before.id == constants.NYAid:
    #             channel = after.voice.voice_channel
    #             if channel and (before.voice.voice_channel != channel):
    #                 state = bot.musicplayer.get_voice_state(before.server)
    #                 if bot.is_voice_connected(before.server):
    #                     if channel == bot.voice_client_in(before.server):
    #                         return
    #                     state.voice = await state.voice.move_to(channel)
    #                 else:
    #                     state.voice = bot.join_voice_channel(channel)

    @bot.event
    async def on_member_update(before, after):
        changed = False
        m = before.server.name + " | Member " + str(before) + " updated: "
        if before.name != after.name:
            m += " name from: " + before.name + " to: " + after.name
            changed = True
        if before.nick != after.nick:
            changed = True
            if not before.nick:
                m += " nick from nothing to: " + after.nick
            else:
                if not after.nick:
                    m += " nick reset"
                else:
                    m += " nick from: " + before.nick + " to: " + after.nick
        for r in before.roles:
            if not r in after.roles:
                m += " -role: " + r.name
                changed = True
        for r in after.roles:
            if not r in before.roles:
                m += " +role: " + r.name
                changed = True
        if before.avatar != after.avatar:
            m += " +avatar changed"
            changed = True
        if changed:
            await log.error(m, filename=before.server.name, serverid=before.server.id)

    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if reaction.emoji == "\N{BROKEN HEART}":
            if reaction.message.author.id == bot.user.id:
                await bot.delete_message(reaction.message)
        if bot.musicplayer:
            await bot.musicplayer.handle_reaction(reaction)

    @bot.event
    async def on_member_ban(member: discord.Member):
        await log.error(member.server.name + " | User " + str(member) + " banned", filename=member.server.name,
                        serverid=member.server.id)

    @bot.event
    async def on_member_unban(server: discord.Server, user: discord.User):
        await log.error("User " + str(user) + " unbanned", filename=server.name, serverid=server.id)

    @bot.event
    async def on_server_join(server: discord.Server):
        user = bot.get_server(constants.PRIVATESERVERid).get_channel(constants.SNOWFLAKE_GENERAL)
        await bot.send_message(user, "I joined a new server named '{}', senpai!".format(server.name))

    @bot.event
    async def on_server_remove(server: discord.Server):
        user = bot.get_server(constants.PRIVATESERVERid).get_channel(constants.SNOWFLAKE_GENERAL)
        await bot.send_message(user, "A new server named '{}' just removed me from service :(".format(server.name))

    return bot


# Start the bot
init_bot().run(secrets.bot_token)
