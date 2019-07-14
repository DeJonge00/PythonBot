#!/usr/bin/env python3
import asyncio
import logging
import traceback

import datetime
import discord
import re
from discord.ext.commands import Bot

import constants
import customHelpFormatter
from database import general as dbcon, rpg as dbconrpg
import log
import message_handler
from secret import secrets
import embedded_list_creator

# Basic configs
pi = 3.14159265358979323846264
REMOVE_JOIN_MESSAGE = False
REMOVE_LEAVE_MESSAGE = False


def initCogs(bot):
    # Add commands
    from comm.admin_commands import Admin
    bot.add_cog(Admin(bot))
    from comm.basic_commands import Basics
    bot.add_cog(Basics(bot))
    from comm.minesweeper import Minesweeper
    bot.add_cog(Minesweeper(bot))
    from comm.hangman import Hangman
    bot.add_cog(Hangman(bot))
    from comm.image_commands import Images
    bot.add_cog(Images(bot))
    from comm.lookup_commands import Lookup
    bot.add_cog(Lookup(bot))
    from comm.trivia import Trivia
    bot.add_cog(Trivia(bot))
    if bot.MUSIC:
        from musicPlayer import MusicPlayer
        bot.musicplayer = MusicPlayer(bot)
        bot.add_cog(bot.musicplayer)
    if bot.RPGGAME:
        from rpggame.rpgmain import RPGGame
        from rpggame.rpggameactivities import RPGGameActivities
        bot.rpggame = RPGGame(bot)
        bot.rpgshop = RPGGameActivities(bot)
        bot.add_cog(bot.rpggame)
        bot.add_cog(bot.rpgshop)
    from comm.mod_commands import Mod
    bot.add_cog(Mod(bot))
    from comm.config_commands import Config
    bot.add_cog(Config(bot))
    from comm.misc_commands import Misc
    bot.add_cog(Misc(bot))


class PythonBot(Bot):
    def __init__(self, music=True, rpggame=True, api=True):
        self.running = True
        self.praise = datetime.datetime.utcnow()
        self.spamlist = []
        self.spongelist = []

        self.commands_counters = {}

        self.MUSIC = music
        self.RPGGAME = rpggame
        self.API = api
        super(PythonBot, self).__init__(command_prefix=secrets.prefix, pm_help=1,
                                        formatter=customHelpFormatter.customHelpFormatter())

    @staticmethod
    def prep_str_for_print(s: str):
        return s.encode("ascii", "replace").decode("ascii")

    @staticmethod
    def pretty_error_str(exception):
        m = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        m = '**{}:** {}```py\n{}```'.format(type(exception).__name__, exception, m)
        return m

    async def _get_prefix(self, message):
        try:
            p = dbcon.get_prefix(message.server.id)
            return p if p else await super(PythonBot, self)._get_prefix(message)
        except (KeyError, AttributeError):
            return await super(PythonBot, self)._get_prefix(message)

    async def delete_message(self, message):
        if not message.channel.is_private:
            try:
                return await super().delete_message(message)
            except discord.Forbidden:
                m = '{} | {} | No permissions to delete message \'{}\''
                m = m.format(message.server.name, message.channel.name, message.content)
                await log.error(m, filename=message.server.name)

    async def send_message(self, destination, content=None, *, tts=False, embed=None):
        try:
            if content:
                try:
                    server = destination.server
                except AttributeError:
                    server = None
                await log.message_content(content, destination, server, self.user, datetime.datetime.now(), [],
                                          "send message:")
            return await super().send_message(destination, content=content, tts=tts, embed=embed)
        except discord.Forbidden:
            if embed:
                m = 'Sorry, it seems I cannot send embedded messages in this channel...'
                await self.send_message(destination, content=m)
            else:
                m = '{} | {} | No permissions to send message \'{}\''
                if isinstance(destination, discord.Channel):
                    m = m.format(destination.server.name, destination.name, content)
                else:
                    m = m.format('direct message', destination.name, content)
                await log.error(m, filename=str(destination))


    async def send_file(self, destination, fp, *, filename=None, content=None, tts=False):
        try:
            return await super().send_file(destination, fp, filename=filename, content=content, tts=tts)
        except discord.Forbidden:
            m = 'Sorry, it seems I cannot send files in this channel...'
            await self.send_message(destination, content=m)

    async def send_typing(self, destination):
        try:
            super().send_typing(destination=destination)
        except discord.Forbidden:
            pass

    async def remove_reaction(self, message, emoji, member):
        try:
            super().remove_reaction(message, emoji, member)
        except discord.Forbidden:
            pass

    @staticmethod
    def command_allowed_in(type: str, identifier: str, command_name: str):
        return command_name == 'togglecommand' or not (dbcon.get_banned_command(type, identifier, command_name) \
               or dbcon.get_banned_command(type, identifier, 'all'))

    @staticmethod
    def command_allowed_in_server(serverid: str, command_name: str):
        split = command_name.split(' ')
        return PythonBot.command_allowed_in('server', command_name, serverid) and (
                len(split) <= 1 or PythonBot.command_allowed_in('server', split[0], serverid))

    @staticmethod
    def command_allowed_in_channel(channelid: str, command_name: str):
        split = command_name.split(' ')
        return PythonBot.command_allowed_in('channel', command_name, channelid) and (
                len(split) <= 1 or PythonBot.command_allowed_in('channel', split[0], channelid))

    async def pre_command(self, message: discord.Message, command: str, is_typing=True, delete_message=True,
                          cannot_be_private=False, must_be_private=False, must_be_nsfw=False, owner_check=False,
                          checks=[]):
        if message.author.id not in [constants.KAPPAid, constants.NYAid]:
            if owner_check:
                await self.bot.send_message(message.channel, "Hahahaha, no")
                await log.message(message, 'Command "{}" used, but owner rights needed'.format(command))
                return False
            elif checks:
                perms = message.channel.permissions_for(message.author)
                check_names = [constants.permissions.get(y) for y in checks]
                if not any([x[1] for x in list(perms) if x[0] in check_names]):
                    await self.bot.send_message(message.channel, "Hahahaha, no")
                    m = 'Command "{}" used, but either of [{}] needed'.format(command, ' '.join(check_names))
                    await log.message(message, m)
                    return False
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
            if must_be_nsfw and not message.channel.name.startswith('nsfw'):
                await self.bot.send_message(message.channel, 'This command cannot be used outside NSFW channels')
                await log.message(message, 'Command "{}" used, but must be an NSFW channel'.format(command))
                return False
            if not self.command_allowed_in_server(command, message.server.id):
                await log.message(message, 'Command "{}" used, but is serverbanned'.format(command))
                return False
            if not self.command_allowed_in_channel(command, message.channel.id):
                await log.message(message, 'Command "{}" used, but is channelbanned'.format(command))
                return False
            if delete_message and dbcon.get_delete_commands(message.server.id):
                await self.delete_message(message)

        await log.message(message, 'Command "{}" used'.format(command))
        if is_typing:
            await self.send_typing(message.channel)
        dbcon.command_counter(command, message)
        return True

    @staticmethod
    def prep_str(s):
        new_s = ''
        for l in s:
            if re.match('[a-zA-Z0-9]', l):
                new_s += l
        return new_s

    async def ask_one_from_multiple(self, message: discord.Message, group: list, question='', errors: dict = {}):
        m = question
        for x in range(min(len(group), 10)):
            m += '\n{}) {}'.format(x + 1, str(group[x]))
        m = await self.say(m)
        r = await self.wait_for_message(timeout=60, author=message.author, channel=message.channel)

        if dbcon.get_delete_commands(message.server.id):
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
            if not (0 <= num < min(10, len(group))):
                raise ValueError
        except ValueError:
            await self.say('That was not a valid number')
            raise
        return group[num]

    # errors = {
    #   'no_mention': No user was mentioned in the message,
    #   'no_user': No user was found with the given name,
    #   'no_reaction': The user did not react to the choice within a minute
    # }
    async def get_member_from_message(self, message: discord.Message, args: list, in_text=False,
                                      errors: dict = {'none': ''}, from_all_members=False) -> discord.Member:
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

        return await self.ask_one_from_multiple(message, users, question='Which user did you mean?')

    async def timeLoop(self):
        await self.wait_until_ready()
        while self.running:
            time = datetime.datetime.utcnow()

            if self.RPGGAME:
                await self.rpggame.game_tick(time)
            if self.MUSIC:
                await self.musicplayer.music_loop(time)

            end_time = datetime.datetime.utcnow()
            # print("Sleeping for " + str(60-(end_time).second) + "s")
            await asyncio.sleep(60 - end_time.second)

    async def quit(self):
        self.running = False
        for key in self.commands_counters.keys():
            print('Command "{}" was used {} times'.format(key, self.commands_counters.get(key)))
        if self.RPGGAME:
            self.rpggame.quit()
        if self.MUSIC:
            await self.musicplayer.quit()

    async def on_member_message(self, member, func_name, text, do_log=True) -> bool:
        if do_log:
            await log.error(member.server.name + " | Member " + str(member) + " just " + text,
                            filename=member.server.name, serverid=member.server.id)
        channel, mes = dbcon.get_message(func_name, member.server.id)
        if not channel or not mes:
            return False
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="User {}!".format(self.prep_str_for_print(text)), value=mes.format(member.name))
        channel = self.get_channel(channel)
        if not channel:
            print('CHANNEL NOT FOUND')
            return False
        m = await self.send_message(channel, embed=embed)
        if REMOVE_JOIN_MESSAGE:
            await asyncio.sleep(30)
            await self.delete_message(m)
        return True


def init_bot():
    bot = PythonBot()
    logging.basicConfig()
    initCogs(bot)
    bot.embed_list = embedded_list_creator.EmbedList(bot)
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

        dbcon.update_server_list(bot.servers)

    # Handle incoming events
    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return
        if message.channel.is_private:
            await log.log("direct message", message.author.name, message.content, "dm")
            for pic in message.attachments:
                await log.message(message, "pic", pic["url"])
            await message_handler.talk(bot, message)
        else:
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
        if bot.RPGGAME and (len(message.content) < 2 or (message.content[:2] == '<@') or (
                message.content[0].isalpha() and message.content[1].isalpha())):
            bot.rpggame.handle(message)

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
        await bot.on_member_message(member, dbcon.WELCOME_TABLE, 'joined')

    @bot.event
    async def on_member_remove(member: discord.Member):
        if member.bot:
            return
        await bot.on_member_message(member, dbcon.GOODBYE_TABLE, 'left')

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
        if before.id == constants.NYAid and before.game != after.game:
            game_name = 'with lolis <3' if not after.game else after.game.name
            await bot.change_presence(game=discord.Game(name=game_name), status=discord.Status.do_not_disturb)
            return
        changed = False
        m = before.server.name + " | Member " + str(before) + " updated: "
        if before.name != after.name:
            m += " name from: " + before.name + " to: " + after.name
            changed = True
            if bot.RPGGAME:
                dbconrpg.set_name(after.id, after.name)
        if before.avatar_url != after.avatar_url and bot.RPGGAME:
            dbconrpg.set_picture(after.id, after.avatar_url)
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
            if r not in after.roles:
                m += " -role: " + r.name
                changed = True
        for r in after.roles:
            if r not in before.roles:
                m += " +role: " + r.name
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
                return
        if bot.musicplayer:
            await bot.musicplayer.handle_reaction(reaction)
        if bot.RPGGAME:
            await bot.rpggame.handle_reaction(reaction)
        if bot.embed_list:
            await bot.embed_list.handle_reaction(reaction)

        await message_handler.reaction(bot, reaction)

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
        m = "I joined a new server named '{}' with {} members, senpai!".format(server.name, server.member_count)
        await bot.send_message(user, m)

    @bot.event
    async def on_server_remove(server: discord.Server):
        user = bot.get_server(constants.PRIVATESERVERid).get_channel(constants.SNOWFLAKE_GENERAL)
        await bot.send_message(user, "A server named '{}' just removed me from service :(".format(server.name))

    return bot

if __name__ == '__main__':
    # Start the bot
    bot = init_bot()
    while bot.running:
        try:
            bot.run(secrets.bot_token)
        except Exception as e:
            tr = traceback.format_exc()
            print(e, tr)
            with open('logs/errors.txt', 'r') as f:
                f.write(tr)
