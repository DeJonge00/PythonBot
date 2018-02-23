import argparse, asyncio, constants, discord, removeMessage, math 
from discord.ext import commands
from collections import deque
from discord.ext.commands import Bot
import urllib.request, urllib.parse, re
embedColor = 0x93cc04

class VoiceEntry:
    def __init__(self, message : discord.Message, player):
        self.requester = message.author
        self.message = message
        self.channel = message.channel
        self.player = player

    def __str__(self):
        return  "'{0}' ({1[0]}.{1[1]}) requested by **{2}**".format(self.player.title, divmod(self.player.duration, 60), self.requester.display_name)

    def embed(self, title="Music"):
        embed = discord.Embed(colour=embedColor)
        embed.set_author(name=title, icon_url=self.requester.avatar_url)
        embed.add_field(name="Title", value=self.player.title + "  ")
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
        self.repeat=False
        self.lastmessage = None

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
                if self.repeat:
                    self.current = VoiceEntry(self.current.message, await self.voice.create_ytdl_player(self.current.player.download_url, before_options=constants.ytdl_before, ytdl_options=constants.ytdl_options, after=self.toggle_next))
                else:
                    self.current = await self.songs.get()
                    await self.bot.send_message(self.current.channel, embed=self.current.embed(title="Now playing"))
                self.current.player.start()
                await self.play_next_song.wait()
                if len(self.songs._queue)==0:
                    await self.bot.send_message(self.current.channel, "The queue is now empty...")
            except Exception as e:
                print(e)
    
    def quit(self):
        self.songs = asyncio.Queue()
        if self.is_playing():
            self.player.stop()

class MusicPlayer:
    def __init__(self, my_bot):
        self.bot = my_bot
        import opuslib
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        state.voice = self.bot.voice_client_in(server)
        return state

    async def stopPlaying(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        state.songs = asyncio.Queue()
        state.skip()
        voiceClient = self.bot.voice_client_in(ctx.message.server)
        if voiceClient != None:
            await voiceClient.disconnect()
        state = None

    async def handleReaction(self, reaction):
        state = self.get_voice_state(reaction.message.server)
        if state != None:
            if state.lastmessage != None:
                if state.lastmessage.id == reaction.message.id:
                    if reaction.emoji=="\N{LEFTWARDS BLACK ARROW}":    #left
                        state = self.get_voice_state(reaction.message.server)
                        await self.showQueue(reaction.message, state.page-1)
                        for m in await self.bot.get_reaction_users(reaction):
                            if m.id != self.bot.user.id:
                                await self.bot.remove_reaction(reaction.message, reaction.emoji, m)
                    if reaction.emoji=="\N{BLACK RIGHTWARDS ARROW}":    #right
                        state = self.get_voice_state(reaction.message.server)
                        await self.showQueue(reaction.message, state.page+1)
                        for m in await self.bot.get_reaction_users(reaction):
                            if m.id != self.bot.user.id:
                                await self.bot.remove_reaction(reaction.message, reaction.emoji, m)

    async def joinVC(self, ctx):
        try:
            channel = ctx.message.author.voice.voice_channel
            if channel == None:
                await self.bot.say("You are not in vc dummy")
                return
            state = self.get_voice_state(ctx.message.server)
            if self.bot.is_voice_connected(ctx.message.server):
                if channel == self.bot.voice_client_in(ctx.message.server).channel:
                    return
                state.voice = await state.voice.move_to(channel)
            else:
                state.voice = await self.bot.join_voice_channel(channel)
        except Exception as e:
            embed = discord.Embed(colour=0x0000FF)
            embed.add_field(name="Something went wrong", value="{}".format(type(e).__name__))
            fmt = '```py\n{}: {}\n```'
            #await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            print(fmt.format(type(e).__name__, e))
            await self.bot.send_message(ctx.message.channel, embed=embed)

    async def playSong(self, ctx, song):
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.joinVC(ctx)
            state = self.get_voice_state(ctx.message.server)
        try:
            player = await state.voice.create_ytdl_player(song, before_options=constants.ytdl_before, ytdl_options=constants.ytdl_options, after=state.toggle_next)
        except Exception as e:
            embed = discord.Embed(colour=0x0000FF)
            embed.add_field(name="Something went wrong", value="{}".format(type(e).__name__))
            fmt = '```py\n{}: {}\n```'
            #await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            print(fmt.format(type(e).__name__, e))
            await self.bot.send_message(ctx.message.channel, embed=embed)
        else:
            player.volume = state.volume
            song = VoiceEntry(ctx.message, player)
            if state.songs.qsize > 0:
                await self.bot.say(embed=song.embed(title="Song added"))
            await state.songs.put(song)

    async def showQueue(self, message : discord.Message, page : int, new=False):
        state = self.get_voice_state(message.server)
        songs = state.songs._queue
        perpage = 10
        state.page = page
        if len(songs) <= 0:
            await self.bot.send_message(message.channel, "The queue is empty! Queue some songs with '{}m q'.".format(constants.prefix))
            return
        if not (0 < page <= math.ceil(len(songs)/perpage)):
            return
        embed = discord.Embed(colour=embedColor)
        embed.set_author(name="Queue: {} songs, {} pages".format(len(songs), math.ceil(len(songs)/perpage)), icon_url=message.author.avatar_url)
        q = ""
        for i in range(10*(page-1), min((10*page), len(songs))):
            q += "{}: '{}' requested by **{}**\n".format(i+1, songs[i].player.title, songs[i].requester.display_name)
        qname = "Queue, page {}/{}".format(page, math.ceil(len(songs)/perpage))
        embed.add_field(name=qname, value=q)
        if new:
            m = await self.bot.send_message(message.channel, embed=embed)
            state.lastmessage = m
            await self.bot.add_reaction(m, '\N{LEFTWARDS BLACK ARROW}')
            await self.bot.add_reaction(m, "\N{BLACK RIGHTWARDS ARROW}")
            await self.bot.add_reaction(m, "\N{BROKEN HEART}")
        else:
            await self.bot.edit_message(message, embed=embed)

    @commands.group(pass_context=1, aliases=["m"], help="'{}help music' for full options".format(constants.prefix))
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            embed = discord.Embed(colour=embedColor)
            embed.set_author(name="Help", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="current", value="Show information about the song currently playing", inline=False)
            embed.add_field(name="join", value="Let me join a voice channel", inline=False)
            embed.add_field(name="leave", value="Send me away from the voice channel", inline=False)
            embed.add_field(name="play", value="'{0}m p' to pause or resume singing, '{0}m p <songname | url>' to add a song to the queue".format(constants.prefix), inline=False)
            embed.add_field(name="queue", value="'{0}m q' to show the queue, '{0}m q <songname | url>' to add a song to the queue".format(constants.prefix), inline=False)
            embed.add_field(name="repeat", value="Repeat the current song", inline=False)
            embed.add_field(name="reset", value="Reset the player for this channel", inline=False)
            embed.add_field(name="skip", value="Vote to skip the current song", inline=False)
            embed.add_field(name="stop", value="Empty the queue and skip the current song, then leave the voice channel", inline=False)
            embed.add_field(name="volume", value="Change the volume of the songs", inline=False)
            await self.bot.say(embed=embed)

    @music.command(pass_context=1, aliases=["c"], help="Show information about the song currently playing")
    async def current(self, ctx):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if state.current == None:
            await self.bot.say("I am not performing at the moment")
            return
        await self.bot.say(embed=state.current.embed())
        return

    @music.command(pass_context=1, aliases=["j"], help="Let me join a voice channel")
    async def join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        state = self.get_voice_state(ctx.message.server)
        force = False
        if (len(args) > 0):
            if (args[0] in ["f", "force"]) & (ctx.message.author.id==constants.NYAid):
                force=True
        if (not(force)) & (state.is_playing()):
            await self.bot.say("Im already singing somewhere else...")
            return
        await self.joinVC(ctx)

    @music.command(pass_context=1, aliases=["l"], help="Send me away from the voice channel")
    async def leave(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        channel = ctx.message.author.voice.voice_channel
        voiceClient = self.bot.voice_client_in(ctx.message.server)
        if voiceClient == None:
            await self.bot.say("I am not in vc dummy")
            return
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            await self.bot.say("I am still singing, use '{}music stop' to send me away".format(constants.prefix))
            return
        await voiceClient.disconnect()

    @music.command(pass_context=1, aliases=["p"], help="'{0}m p' to pause or resume singing, '{0}m p <songname | url>' to add a song to the queue".format(constants.prefix))
    async def play(self, ctx, *song):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(song) > 0:
            await self.playSong(ctx, " ".join(song))
            return 
        state = self.get_voice_state(ctx.message.server)
        if state.current == None:
            await self.bot.say("There is nothing to sing")
            return
        if state.is_playing():
            if state.player.is_playing():
                state.player.pause()
                await self.bot.say(ctx.message.author.display_name + " paused my singing...")
                return
            else:
                state.player.resume()
                await self.bot.say("Singing resumed")
                return
        await self.bot.say("I DUNNO WHAT TO DO ;-;")

    @music.command(pass_context=1, aliases=["q"], help="'{0}m q' to show the queue, '{0}m q <songname | url>' to add a song to the queue".format(constants.prefix))
    async def queue(self, ctx, *song):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(song) <= 0:
            return await self.showQueue(ctx.message, 1, new=True)
        await self.playSong(ctx, " ".join(song))
    
    @music.command(pass_context=1, aliases=["r"], help="Repeat the current song")
    async def repeat(self, ctx, *song):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if state.voice == None:
            await self.bot.say("I am not singing at the moment")
            return
        if ctx.message.author.voice_channel != state.voice.channel:
            await self.bot.say("You are not here with me...")
            return
        if state.repeat:
            state.repeat = False
            await self.bot.say("Repeat is now off")
            return
        state.repeat = True
        await self.bot.say("Repeat is now on")

    @music.command(pass_context=1, help="Reset the player for this channel")
    async def reset(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        await self.stopPlaying(ctx)
        try:
            self.voice_states.pop(server.id)
        except KeyError as e:
            print(e)

    @music.command(pass_context=1, aliases=["s"], help="Vote to skip a song, or just skip it if you are the requester")
    async def skip(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        state = self.get_voice_state(ctx.message.server)
        if state.voice == None:
            await self.bot.say("I am not plaing songs right now...")
            return
        if ctx.message.author.voice_channel != state.voice.channel:
            await self.bot.say("You are not in the right voice channel for this command")
            return

        force = False
        if (len(args) > 0):
            if (args[0] in ["f", "force"]) & (ctx.message.author.id==constants.NYAid):
                force=True
            else:
                try:
                    n = int(args[0])-1
                except ValueError:
                    await self.bot.say("I'm not sure that's a number...")
                    return
                songs = list(state.songs._queue)
                print(songs)
                if n >= len(songs):
                    await self.bot.say("The song queue is not that long...")
                if (ctx.message.author.id==songs[n].requester.id) | (ctx.message.author.id==constants.NYAid):
                    s = songs[n]
                    del songs[n]
                    print(songs)
                    state.songs._queue = deque(songs)
                    print("Q")
                    print(state.songs._queue)
                    await self.bot.say("Removed a song from the queue: {}".format(s))
                    return
                else:
                    await self.bot.say("Only the requester, {}, can skip that song".format(songs[n].requester.name))
                    return
        state.skip_votes.add(ctx.message.author.id)
        votesNeeded = math.ceil(len(self.bot.voice_client_in(ctx.message.server).channel.voice_members)/3)
        votes = len(state.skip_votes)
        if votes >= votesNeeded:
            state.skip()
            await self.bot.say("{} people voted to skip the song\nSkipping now!".format(votes))
            return
        if (force) | (state.current.requester.id==ctx.message.author.id):
            state.skip()
            await self.bot.say("Master has decided to skip this song!")
            return
        await self.bot.say("Votes to skip: {}/{}".format(votes,votesNeeded))

    @music.command(pass_context=1, aliases=["quit"], help="Empty the queue and skip the current song, then leave the voice channel")
    async def stop(self, ctx):
        await removeMessage.deleteMessage(self.bot, ctx)
        await self.stopPlaying(ctx)
        await self.bot.say("Baibai o/")

    @music.command(pass_context=1, aliases=["v"], help="Change the volume of the songs")
    async def volume(self, ctx, vol : int):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        state = self.get_voice_state(ctx.message.server)
        if not 0 < vol < 200:
            await self.bot.say("Volume must be between 0 and 200")
            return
        state.volume = vol/100
        if state.is_playing():
            state.player.volume = vol/100
        await self.bot.say("Volume set to {}%".format(vol))

    def quit(self):
        for s in self.voice_states.values():
            s.quit()
