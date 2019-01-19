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
    @commands.command(pass_context=1, help="Trivia", aliases=["tr"])
    async def trivia(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command="trivia"):
            return
        if len(args) <= 0:
            prefix = await self.bot._get_prefix(ctx.message)
            await self.bot.say("[Usage] To start a new game use: {}trivia new".format(prefix))
            return

        if args[0] == "cat" or args[0] == "categories":
            await self.display_categories()
            return

        if args[0] == "new":
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
            try:
                del self.game_instances[ctx.message.channel]
            except KeyError as e:
                print(e)

        if args[0] == "join":
            if ctx.message.channel in self.game_instances:
                await self.game_instances[ctx.message.channel].player_turn_join(ctx.message.author)
            else:
                await self.bot.say(ctx.message.author.mention + " there's currently no running game on this channel.")

        if args[0] == "quit":
            if ctx.message.channel in self.game_instances:
                await self.game_instances[ctx.message.channel].player_quit(ctx.message.author)
            else:
                await self.bot.say(ctx.message.author.mention + " there's currently no running game on this channel.")

    async def display_categories(self):
        display_cat = "Triva categories are: \n"
        for cat in self.categories:
            display_cat += (str(cat['id']) + ") " + cat['name'] + ".\n")
        await self.bot.say(display_cat)
