import argparse, asyncio, secret.constants as constants, discord, removeMessage, math
from discord.ext import commands
from discord.ext.commands import Bot
import urllib.request, urllib.parse, re

embedColor = 0x710075

class VoiceEntry:
    def __init__(self, message : discord.Message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        return self.requester.display_name + " requested: " + self.player.title + " (" + self.player.duration + ")"

    def embed(self):
        return self.embed("")

    def embed(self, title : str):
        embed = discord.Embed(colour=embedColor)
        embed.add_field(name="Requester", value=self.requester.display_name)
        embed.add_field(name="Title", value=self.player.title)
        embed.add_field(name="Duration", value=self.player.duration)
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
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.say(embed=current.embed("Now playing"))
            self.current.player.start()
            await self.play_next_song.wait()

    def quit(self):
        self.songs = asyncio.Queue()
        if self.is_playing():
            self.player.stop()

class MusicPlayer:
    def __init__(self, my_bot):
        self.bot = my_bot
        discord.opus.load_opus("opus.dll")
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        return state

    @commands.group(pass_context=1, aliases=["m"])
    async def music(self, ctx):
        print("Music command used")
        if ctx.invoked_subcommand is None:
            await self.bot.say('Choose from: join (j)", leave (l), play (p), skip (s)')

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

    @music.command(name="join", pass_context=1, aliases=["j"])
    async def _join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        await self.joinVC(ctx)

    @music.command(name="leave", pass_context=1, aliases=["l"])
    async def _leave(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        channel = ctx.message.author.voice.voice_channel
        voiceClient = self.bot.voice_client_in(ctx.message.server)
        if voiceClient == None:
            return await self.bot.say("I am not in vc dummy")
        await voiceClient.disconnect()

    @music.command(name="play", pass_context=1, hidden=1, aliases=["p"])
    async def _play(self, ctx, song : str):
        print(song)
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.joinVC(ctx)
            state = self.get_voice_state(ctx.message.server)
        try:
            player = await state.voice.create_ytdl_player(song, before_options=constants.ytdl_before, ytdl_options=constants.ytdl_options, after=state.toggle_next)
        except Exception as e:
            embed = discord.Embed(colour=0x0000FF)
            embed.add_field(name="Something went wrong", value="Cannot play selected song")
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            song = VoiceEntry(ctx.message, player)
            await self.bot.say(embed=song.embed())
            await state.songs.put(song)

    @music.command(name="volume", pass_context=1, hidden=1, aliases=["v"])
    async def _volume(self, ctx, vol : int):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if not 0 < vol < 200:
            return await self.bot.say("Volume must be between 0 and 200")
        state.current.volume = vol/100

    @music.command(name="skip", pass_context=1, hidden=1)
    async def _skip(self, ctx, vol : int):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        state.skip_votes.add(ctx.message.author.id)
        votesNeeded = math.ceil(len(self.bot.voice_client_in(ctx.message.server).channel.voice_members)/3)
        await self.bot.say("Votes: " + str(len(state.skip_votes)) + "/" + str(votesNeeded))
        if state.skip_votes > votesNeeded:
            state.skip()

    def quit(self):
        for x in self.voice_states.values():
            x.quit()