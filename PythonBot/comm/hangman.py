import comm.hangmaninstance
from comm.hangmaninstance import MAXFAULTS
import constants
import discord
import random
import string
from discord.ext import commands
from secret.secrets import prefix

RIGHT = 0
WRONG = 1
GAMEOVER = 2
WIN = 3

EMBEDCOLOR = 0x007a01


# Normal commands
class Hangman:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.games = {}
        self.prev = {}
        print('Hangman started')

    # {prefix}hangman <create,new> {custom | sentence} | <guess>
    @commands.command(pass_context=1, help="Hangman game", aliases=["hm"])
    async def hangman(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='hangman'):
            return
        gameinfo = ('user', ctx.message.author.id) if ctx.message.channel.is_private else ('channel', ctx.message.channel.id)
        game = self.games.get(gameinfo)

        if len(args) <= 0:
            if not game:
                await self.bot.say(
                    "Create a new game by using the command {}hangman <create> [custom | sentence]".format(prefix))
                return
            else:
                await self.bot.say("Guess a letter or the sentence by using >hangman <guess>!")
                return

        if not game:
            # New game
            if args[0].lower() in ["create", "new"]:
                if len(args) >= 2:
                    if args[1] == "custom":
                        await self.bot.send_message(ctx.message.author,
                                                    "Hi there!\nWhat would you like the sentence for the hangman game to be?")
                        m = await self.bot.wait_for_message(timeout=60, author=ctx.message.author,
                                                            check=Hangman.is_private_check)
                        if not m:
                            await self.bot.say(
                                "Senpai hasn't responded in a while, I guess we will stop playing then...")
                            return
                        if m.content.startswith('create') or m.content.startswith('new'):
                            await self.bot.say('Sorry, the word cannot begin with create or new for technical reasons...')
                            return
                        word = m.content
                    else:
                        word = " ".join(args[1:])
                else:
                    r = random.randint(0, len(constants.hangmanwords) - 1)
                    word = constants.hangmanwords[r]
                g = comm.hangmaninstance.HangmanInstance(word)
                self.games[gameinfo] = g
                return await self.show(ctx.message.channel, g, "New game initialized")
            return await self.bot.say("There is no game running in this server b-b-baka")
        # Guess sentence
        if " ".join(args).lower().translate(str.maketrans('', '', string.punctuation)) == game.word.lower().translate(
                str.maketrans('', '', string.punctuation)):
            self.games.pop(gameinfo)
            await self.show(ctx.message.channel, game, message=ctx.message.author.name, win=True)
            return
        if len(args[0]) > 1:
            game.faults += 1
            if game.faults >= MAXFAULTS:
                self.games.pop(gameinfo)
            await self.show(ctx.message.channel, game, "Sorry, the word was not \"" + " ".join(args) + "\"...")
            return
        # Guess letter
        result = game.guess(args[0])
        if result == WIN:
            self.games.pop(gameinfo)
            await self.show(ctx.message.channel, game, message=ctx.message.author.name, win=True)
            return
        if result == RIGHT:
            await self.show(ctx.message.channel, game,
                            "You guessed right, the letter \"" + " ".join(args) + "\" is in the sentence")
            return
        if result == WRONG:
            await self.show(ctx.message.channel, game,
                            "Sorry, the letter \"" + " ".join(args) + "\" is not in the sentence")
            return
        if result == GAMEOVER:
            self.games.pop(gameinfo)
            await self.show(ctx.message.channel, game)
            return

    async def show(self, channel: discord.Channel, game: comm.hangmaninstance.HangmanInstance, message="", win=False):
        embed = discord.Embed(colour=EMBEDCOLOR)
        if win:
            embed.add_field(name="Congratulations on winning", value=message, inline=False)
            embed.set_thumbnail(url="http://nobacks.com/wp-content/uploads/2014/11/Golden-Star-3-500x500.png")
            embed.add_field(name="The sentence was indeed", value=game.word)
        else:
            if game.faults >= 6:
                embed.add_field(name="YOU DIED", value="Better luck next time!", inline=False)
                embed.set_thumbnail(url="http://i.imgur.com/1IXbcNb.png")
                embed.add_field(name="The sentence", value=game.word)
            else:
                embed.add_field(name="Message", value=message, inline=False)
                if game.faults == 1:
                    embed.set_thumbnail(url="http://i.imgur.com/nwXZ5Ef.png")
                if game.faults == 2:
                    embed.set_thumbnail(url="http://i.imgur.com/izSXiI6.png")
                if game.faults == 3:
                    embed.set_thumbnail(url="http://i.imgur.com/D1BsiYo.png")
                if game.faults == 4:
                    embed.set_thumbnail(url="http://i.imgur.com/sqdAuTl.png")
                if game.faults == 5:
                    embed.set_thumbnail(url="http://i.imgur.com/ZHXq151.png")

                embed.add_field(name="Guessed so far", value=str(game), inline=False)
                if len(game.wrongguesses) > 0:
                    embed.add_field(name="Letters guessed wrong", value=" ".join(game.wrongguesses))
                embed.add_field(name="Faults", value=str(game.faults) + "/6")
        m = await self.bot.send_message(channel, embed=embed)
        if channel.id in self.prev.keys():
            try:
                await self.bot.delete_message(self.prev.get(channel.id))
            except discord.Forbidden:
                print(m.server.name + " | No permission to delete messages")
        if not channel.is_private:
            if game.faults >= 6:
                self.prev[channel.id] = None
            else:
                self.prev[channel.id] = m

    @staticmethod
    def is_private_check(msg):
        return msg.channel.is_private
