import discord
from discord.ext import commands

from comm.battleship_game import BattleshipGame

EMBEDCOLOR = 0x007a01


# Normal commands
class Battleships:
    def __init__(self, my_bot: discord.Client):
        self.bot = my_bot
        self.games = {}
        self.prev = {}
        print('Battleships started')

    # {prefix}hangman <create,new> {custom | sentence} | <guess>
    @commands.group(pass_context=1, help="Multiplayer Battleship game", aliases=["bs"])
    async def battleship(self, ctx):
        pass

    @battleship.command(pass_context=1, help="Create new game", aliases=["create", 'n', 'c'])
    async def new(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='battleship new', cannot_be_private=True):
            return

        if self.games.get(ctx.message.author.id):
            await self.bot.say('You are currently busy in a game, continue or quit that one first')
            return

        try:
            opponent = await self.bot.get_member_from_message(ctx.message, args)
        except ValueError:
            return

        game = BattleshipGame(self.bot, ctx.message.author.id, opponent.id)
        self.games[ctx.message.author.id] = game
        self.games[opponent.id] = game

        await game.start()

    @battleship.command(pass_context=1, help="Place a ship", aliases=["p", 's', 'ship'])
    async def place(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='battleship place', must_be_private=True):
            return
        try:
            await self.games.get(ctx.message.author.id).set_ship(ctx.message.author.id, *args)
        except KeyError:
            await self.bot.say('Start a game with `{}battleship create <person>` in a server'.format(self.bot._get_prefix(ctx.message)))

    @battleship.command(pass_context=1, help="Guess", aliases=["g"])
    async def guess(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='battleship guess', must_be_private=True):
            return

        if len(args) < 1:
            await self.bot.say('Use this command with `{0}battleship guess <coordinate>`, for example: `{0}bs g b4`'
                               .format(self.bot._get_prefix(ctx.message)))
            return

        try:
            await self.games.get(ctx.message.author.id).guess(ctx.message.author.id, args[0])
        except AttributeError:
            await self.bot.say('You haven\t started a game with anyone...')
            return

    @battleship.command(pass_context=1, help="Quit your current game", aliases=["q", 'stop'])
    async def quit(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='battleship guess', must_be_private=True):
            return

        try:
            game = self.games.get(ctx.message.author.id)
        except AttributeError:
            await self.bot.say('You haven\'t started a game with anyone...')
            return

        game.quit()
        await game.send_message(game.p1, 'The battleship game has been aborted')
        await game.send_message(game.p2, 'The battleship game has been aborted')
