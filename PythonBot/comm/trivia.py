from discord.ext import commands
import json
import requests
from comm import triviainstance


CATEGORIES_URL = "https://opentdb.com/api_category.php"


class Trivia:
    def __init__(self, mybot):
        self.bot = mybot
        self.categories = self.categories = json.loads(requests.get(url=CATEGORIES_URL).text)['trivia_categories']
        self.game_instances = {}
        print("Trivia started")

    # {prefix}trivia <categories>
    @commands.group(pass_context=1, help="Trivia", aliases=['tr'])
    async def trivia(self, ctx):
        if not ctx.invoked_subcommand:
            prefix = await self.bot._get_prefix(ctx.message)
            await self.bot.say("[Usage] To start a new game use: {}trivia new".format(prefix))
        return

    @trivia.command(pass_context=1, aliases=['categories'])
    async def cat(self):
        display_cat = "Triva categories are: \n"
        for cat in self.categories:
            display_cat += (str(cat['id']) + ") " + cat['name'] + ".\n")
        await self.bot.say(display_cat)
        return

    @trivia.command(pass_context=1)
    async def new(self, ctx):
        if ctx.message.channel in self.game_instances:
            await self.bot.say("There's already a trivia game on this channel!")
            return
        await self.bot.say("New trivia game requested!\nPlease chose a game mode: 1)time attack  2)turn by turn")
        game_mode = await self.bot.wait_for_message(channel=ctx.message.channel, author=ctx.message.author)
        if game_mode.content == '1':
            await self.bot.say("Time attack mode selected!")
            game_mode = "time"
        elif game_mode.content == '2':
            await self.bot.say("Turn by turn mode selected!")
            game_mode = "turn"
        else:
            await self.bot.say(ctx.message.author.mention + " stop wasting my time.")
            return
        self.game_instances[ctx.message.channel] = triviainstance.TriviaInstance(
            my_bot=self.bot, channel=ctx.message.channel, author=ctx.message.author,
            categories=self.categories, mode=game_mode)
        # get game parameters, then start and play it until the end
        await self.game_instances[ctx.message.channel].get_params(ctx)
        # goobye fren
        self.delete_instance(ctx.message.channel)
        return

    @trivia.command(pass_context=1)
    async def join(self, ctx):
        if await self.is_game_running(ctx.message.channel, ctx.message.author):
            await self.game_instances[ctx.message.channel].player_turn_join(ctx.message.author)
        return

    @trivia.command(pass_context=1)
    async def quit(self, ctx):
        if await self.is_game_running(ctx.message.channel, ctx.message.author):
            await self.game_instances[ctx.message.channel].player_quit(ctx.message.author)
        return

    @trivia.command(pass_context=1)
    async def cancel(self, ctx):
        if await self.is_game_running(ctx.message.channel, ctx.message.author):
            if self.game_instances[ctx.message.channel].game_creator == ctx.message.author:
                self.game_instances[ctx.message.channel].stop_playing()
                self.delete_instance(ctx.message.channel)
            else:
                await self.bot.say(ctx.message.author.mention + " only the game creator can cancel the game")
        return

    def delete_instance(self, channel):
        try:
            del self.game_instances[channel]
        except KeyError as e:
            print(e)

    async def is_game_running(self, channel, author):
        if channel in self.game_instances:
            return True
        await self.bot.say(author.mention + " there's currently no running game on this channel.")
        return False
