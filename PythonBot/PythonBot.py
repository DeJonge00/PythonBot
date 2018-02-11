#!/usr/bin/env python3
import asyncio, discord
from discord.ext import commands
from discord.ext.commands import Bot
import customHelpFormatter, datetime, log, logging, message_handler, pickle, random, sys, sqlite3, constants
from secret import secrets

# Basic configs
pi = 3.14159265358979323846264
REMOVE_JOIN_MESSAGE = False
REMOVE_LEAVE_MESSAGE = False

def initCogs(bot):
    # Add commands
    import comm.basic_commands
    bot.add_cog(comm.basic_commands.Basics(bot))
    import comm.minesweeper
    bot.add_cog(comm.minesweeper.Minesweeper(bot))
    import comm.hangman
    bot.add_cog(comm.hangman.Hangman(bot))
    import comm.image_commands
    bot.add_cog(comm.image_commands.Images(bot))
    if bot.MUSIC:
        import musicPlayer
        bot.musicplayer = musicPlayer.MusicPlayer(bot)
        bot.add_cog(bot.musicplayer)
    if bot.RPGGAME:
        import rpggame.rpgmain, rpggame.rpgshop
        bot.rpggame = rpggame.rpgmain.RPGGame(bot)
        bot.rpgshop = rpggame.rpgshop.RPGShop(bot)
        bot.add_cog(bot.rpggame)
        bot.add_cog(bot.rpgshop)
    import comm.mod_commands
    bot.add_cog(comm.mod_commands.Mod(bot))
    import comm.misc_commands
    bot.add_cog(comm.misc_commands.Misc(bot))

class PythonBot(Bot):
    def __init__(self, music=True, rpggame=True):
        self.praise = datetime.datetime.utcnow()
        self.spamlist = []
        self.spongelist = []
        self.MUSIC = music
        self.RPGGAME = rpggame
        super(PythonBot, self).__init__(command_prefix=commands.when_mentioned_or(constants.prefix), pm_help=1, formatter=customHelpFormatter.customHelpFormatter())

def initBot():
    bot = PythonBot()
    logging.basicConfig()
    initCogs(bot)

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
        try:
            if (message.author.bot):
                return
            if (message.channel.is_private):
                print(message.author.name + " | said in dm's: " + message.content)
            else:
                if (message.server.id == constants.NINECHATid) & (message.server.get_member(constants.NYAid)==None):
                    print(message.server.name + "-" + message.channel.name + " (" + message.user.name + ") " + message.content)
                if message.content:
                    await message_handler.new(bot, message)
            if len(message.attachments) > 0:
                await message_handler.new_pic(bot, message)
            # Commands in the message
            await bot.process_commands(message)
            # Send message to rpggame for exp
            if bot.RPGGAME:
                await bot.rpggame.handle(message)
        except Exception as e:
            log.error(str(e))
    @bot.event
    async def on_message_edit(before, after):
        await message_handler.edit(before)
    @bot.event
    async def on_message_delete(message):
        await message_handler.deleted(message)
    @bot.event
    async def on_member_join(member):
        await log.error(member.server.name + " | Member " + member.name + " just joined", filename=member.server.name)
        conn = sqlite3.connect(constants.WELCOMEMESSAGEFILE)
        c = conn.cursor()
        c.execute("SELECT message FROM welcome WHERE serverID=" + member.server.id)
        mes = c.fetchone()
        conn.commit()
        conn.close()
        if mes == None:
            return
        mes = mes[0]
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="User joined!", value=mes.format(member.mention))
        m = await bot.send_message(member.server.default_channel, embed=embed)
        if REMOVE_JOIN_MESSAGE:
            await asyncio.sleep(30)
            try:
                await bot.delete_message(m)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
    @bot.event
    async def on_member_remove(member):
        await log.error(member.server.name + " | Member " + member.name + " just left", filename=member.server.name)
        conn = sqlite3.connect(constants.GOODBYEMESSAGEFILE)
        c = conn.cursor()
        c.execute("SELECT message FROM goodbye WHERE serverID=" + member.server.id)
        mes = c.fetchone()
        conn.commit()
        conn.close()
        if mes == None:
            return
        mes = mes[0]
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="User left!", value=mes.format(member.mention))
        m = await bot.send_message(member.server.default_channel, embed=embed)
        if REMOVE_LEAVE_MESSAGE:
            await asyncio.sleep(30)
            try:
                await bot.delete_message(m)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")
    @bot.event
    async def on_channel_delete(channel):
        await log.error("deleted channel: " + channel.name, filename=channel.server.name)
    @bot.event
    async def on_channel_create(channel):
        if channel.is_private:
            await log.error("created private channel", filename="private")
        else:
            await log.error("created channel: " + channel.name, filename=channel.server.name)
    @bot.event
    async def on_channel_update(before, after):
        m = "Channel updated:"
        if before.id != after.id:
            m += " id from: " + before.id + " to: " + after.id
        if before.name != after.name:
            m += " name from: " + before.name + " to: " + after.name
        if before.position != after.position:
            m += " position from: " + str(before.position) + " to: " + str(after.position)
        if before._permission_overwrites != after._permission_overwrites:
            m += " _permission_overwrites changed"
        await log.error(m, filename=before.server.name)
    @bot.event
    async def on_voice_state_update(before, after):
        if bot.MUSIC:
            if before.id == constants.NYAid:
                channel = after.voice.voice_channel
                if (channel != None) & (before.voice.voice_channel != channel):
                    state = bot.musicplayer.get_voice_state(before.server)
                    if bot.is_voice_connected(before.server):
                        if channel == bot.voice_client_in(before.server):
                            return
                        state.voice = await state.voice.move_to(channel)
                    else:
                        state.voice = await bot.join_voice_channel(channel)
    @bot.event
    async def on_member_update(before, after):
        changed = False
        m = before.server.name + " | member " + before.name + " updated: "
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
            m += " avatar changed"
            changed = True
        if changed:
            await log.error(m, filename=before.server.name)
    @bot.event
    async def on_server_update(before, after):
        m = "server " + before.name + " updated: "
        if before.name != after.name:
            m += " name from: " + before.name + " to: " + after.name
        for r in before.roles:
            if not r in after.roles:
                m += " -role: " + r.name
        for r in after.roles:
            if not r in before.roles:
                m += " +role: " + r.name
        if before.region != after.region:
            m += " region from: " + before.region + " to: " + after.region
        if not m == "server " + before.name + " updated: ":
            await log.error(m, filename=before.server.name)
    @bot.event
    async def on_server_role_update(before, after):
        m = "Role " + before.name + " updated: "
        if before.name != after.name:
            m += " name from: " + before.name + " to: " + after.name
        for r in before.permissions:
            if not r in after.permissions:
                x, y = r
                if y:
                    m += " -permission: " + x
        for r in after.permissions:
            if not r in before.permissions:
                x, y = r
                if y:
                    m += " +permission: " + x
        if not m == "role " + before.name + " updated: ":
            await log.error(m, filename=before.server.name)
    @bot.event
    async def on_server_emojis_update(before, after):
        m = "emojis updated: "
        if len(before) != len(after):
            m += " size from: " + str(len(before)) + " to: " + str(len(after))
        if not "emojis updated: ":
            await log.error(m, filename=before.server.name)
    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if (reaction.emoji=="\N{BROKEN HEART}") | (reaction.message.author.id==constants.NYAid):
            if reaction.message.author.id == bot.user.id:
                await bot.delete_message(reaction.message)
        if musicplayer:
            await bot.musicplayer.handleReaction(reaction)
    @bot.event
    async def on_member_ban(member):
        await log.error("user " + member.name + " banned", filename=member.server.name)
    @bot.event
    async def on_member_unban(member):
        await log.error("user " + member.name + " unbanned", filename=member.server.name)
    return bot

# Start the bot
initBot().run(secrets.bot_token)