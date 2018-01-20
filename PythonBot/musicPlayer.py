import argparse, asyncio, secret.constants as constants, discord, removeMessage, math
from discord.ext import commands
from discord.ext.commands import Bot
import urllib.request, urllib.parse, re

embedColor = 0x93cc04

class VoiceEntry:
    def __init__(self, message : discord.Message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        return self.requester.display_name + " requested: " + self.player.title + " (" + self.player.duration + ")"

    def embed(self, title="Music"):
        embed = discord.Embed(colour=embedColor)
        embed.set_author(name=title, icon_url=self.requester.avatar_url)
        embed.add_field(name="Title", value=self.player.title + " ")
        embed.add_field(name="Duration", value="{0[0]}m {0[1]}s".format(divmod(self.player.duration, 60)))
        embed.add_field(name="Requester", value=self.requester.display_name)
        if self.player.likes != None:
            embed.add_field(name="👍", value=self.player.likes)
        if self.player.dislikes != None:
            embed.add_field(name="👎", value=self.player.dislikes)
        return embed

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.volume = 1.0

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False
        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            try:
                self.play_next_song.clear()
                self.current = await self.songs.get()
                await self.bot.send_message(self.current.channel, embed=self.current.embed(title="Now playing"))
                self.current.player.start()
                await self.play_next_song.wait()
            except Exception as e:
                print(e)
    
    def quit(self):
        self.songs = asyncio.Queue()
        if self.is_playing():
            self.player.stop()

class MusicPlayer:
    def __init__(self, my_bot):
        self.bot = my_bot
        try:
            discord.opus.load_opus("opus.dll")
        except:
            print("Failed to load opus.dll")
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        state.voice = self.bot.voice_client_in(server)
        return state

    @commands.group(pass_context=1, aliases=["m"], help="'>music' for full options")
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            embed = discord.Embed(colour=embedColor)
            embed.set_author(name="Help", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="current", value="Show information about the song currently playing", inline=False)
            embed.add_field(name="join", value="Let me join a voice channel", inline=False)
            embed.add_field(name="leave", value="Send me away from the voice channel", inline=False)
            embed.add_field(name="play", value="'>m p' to pause or resume singing, '>m p <songname | url>' to add a song to the queue", inline=False)
            embed.add_field(name="queue", value="'>m q' to show the queue, '>m q <songname | url>' to add a song to the queue", inline=False)
            embed.add_field(name="skip", value="Vote to skip the current song", inline=False)
            embed.add_field(name="stop", value="Empty the queue and skip the current song, then leave the voice channel", inline=False)
            embed.add_field(name="volume", value="Change the volume of the songs", inline=False)
            await self.bot.say(embed=embed)

    async def joinVC(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        if channel == None:
            return await self.bot.say("You are not in vc dummy")
        state = self.get_voice_state(ctx.message.server)
        if self.bot.is_voice_connected(ctx.message.server):
            if channel == self.bot.voice_client_in(ctx.message.server):
                return await self.bot.say("Present o/")
            state.voice = await state.voice.move_to(channel)
        else:
            state.voice = await self.bot.join_voice_channel(channel)

    async def play(self, ctx, song):
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.joinVC(ctx)
            state = self.get_voice_state(ctx.message.server)
        try:
            player = await state.voice.create_ytdl_player(song, before_options=constants.ytdl_before, ytdl_options=constants.ytdl_options, after=state.toggle_next)
        except Exception as e:
            embed = discord.Embed(colour=0x0000FF)
            embed.add_field(name="Something went wrong", value="Cannot play selected song")
            #fmt = '```py\n{}: {}\n```'
            #await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            player.volume = state.volume
            song = VoiceEntry(ctx.message, player)
            await self.bot.say(embed=song.embed(title="Song added"))
            await state.songs.put(song)

    @music.command(name="current", pass_context=1, aliases=["c"])
    async def _current(self, ctx):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if state.current == None:
            return await self.bot.say("I am not performing at the moment")
        return await self.bot.say(embed=state.current.embed())

    @music.command(name="join", pass_context=1, aliases=["j"])
    async def _join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        state = self.get_voice_state(ctx.message.server)
        force = False
        if (len(args) > 0) & (args[0] in ["f", "force"]) & (ctx.message.author.id==constants.NYAid):
            force=True
        if (not(force)) & (state.is_playing()):
            return await self.bot.say("Im already singing somewhere else...")
        await self.joinVC(ctx)

    @music.command(name="leave", pass_context=1, aliases=["l"])
    async def _leave(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        channel = ctx.message.author.voice.voice_channel
        voiceClient = self.bot.voice_client_in(ctx.message.server)
        if voiceClient == None:
            return await self.bot.say("I am not in vc dummy")
        await voiceClient.disconnect()

    @music.command(name="play", pass_context=1, aliases=["p"])
    async def _play(self, ctx, *song):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(song) > 0:
            return await self.play(ctx, " ".join(song))
        state = self.get_voice_state(ctx.message.server)
        if state.current == None:
            return await self.bot.say("There is nothing to sing")
        if state.is_playing():
            if state.player.is_playing():
                state.player.pause()
                return await self.bot.say(ctx.message.author.display_name + " paused my singing...")
            else:
                state.player.resume()
                return await self.bot.say("Singing resumed")
        await self.bot.say("I DUNNO WHAT TO DO ;-;")

    @music.command(name="queue", pass_context=1, aliases=["q"])
    async def _queue(self, ctx, *song):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(song) <= 0:
            state = self.get_voice_state(ctx.message.server)
            songs = state.songs._queue
            if len(songs) <= 0:
                return await self.bot.say("There is nothing left, queue some songs with '>music queue'")
            embed = discord.Embed(colour=embedColor)
            embed.set_author(name="Queue", icon_url=ctx.message.author.avatar_url)
            q = ""
            i = 1
            for s in songs:
                q += str(i) + ": '" + s.player.title + "' requested by **" + s.requester.display_name + "**\n"
                if i >= 9:
                    break
                i += 1
            embed.add_field(name="Queue", value=q)
            return await self.bot.say(embed=embed)
        return await self.play(ctx, " ".join(song))
    
    @music.command(name="skip", pass_context=1, aliases=["s"])
    async def _skip(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        force = False
        if (len(args) > 0):
            if (args[0] in ["f", "force"]) & (ctx.message.author.id==constants.NYAid):
                force=True
        state.skip_votes.add(ctx.message.author.id)
        votesNeeded = math.ceil(len(self.bot.voice_client_in(ctx.message.server).channel.voice_members)/3)
        votes = len(state.skip_votes)
        if votes >= votesNeeded:
            state.skip()
            return await self.bot.say(str(votes) + " people voted to skip the song\nSkipping now!")
        if (force) | (state.current.requester.id==ctx.message.author.id):
            state.skip()
            return await self.bot.say("Master has decided to skip this song!")
        await self.bot.say("Votes to skip: " + str(votes) + "/" + str(votesNeeded))

    @music.command(name="stop", pass_context=1, aliases=["quit"])
    async def _stop(self, ctx):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        state.songs = asyncio.Queue()
        state.skip()
        voiceClient = self.bot.voice_client_in(ctx.message.server)
        if voiceClient != None:
            await voiceClient.disconnect()
        await self.bot.say("Baibai o/")

    @music.command(name="volume", pass_context=1, aliases=["v"])
    async def _volume(self, ctx, vol : int):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        state = self.get_voice_state(ctx.message.server)
        if not 0 < vol < 200:
            return await self.bot.say("Volume must be between 0 and 200")
        state.volume = vol/100
        if state.is_playing():
            state.player.volume = vol/100
        await self.bot.say("Volume set to " + str(vol) + "%")

    def quit(self):
        for s in self.voice_states.values():
            s.quit()