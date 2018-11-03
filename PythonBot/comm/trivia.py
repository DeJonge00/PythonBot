from discord.ext import commands
import discord
import json
import html
import requests
import re
import random

# this game has been made with the open trivia db API : https://opentdb.com/
# All data provided by the API is available under the Creative Commons Attribution-ShareAlike 4.0 International License.


class Trivia:
    """Init Trivia game with the number of questions, their category, difficulty and type (boolean or multiple)"""
    def __init__(self, my_bot):
        self.bot = my_bot
        self.questions_nb = "10"
        self.category = ""
        self.difficulty = ""
        self.type = ""
        print("Trivia started")

    # {prefix}trivia <categories>
    @commands.command(pass_context=1, help="Trivia categories", aliases=["tr"])
    async def trivia(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='trivia'):
            return
        if len(args) <= 0:
            await self.bot.say(
                "Start a new game with >trivia new <questions nbr> <category> <difficulty> <type> <mode>\n" +
                "If nothing is specified, the game will start with 10 questions and the rest will be random.\n" +
                "You can see categories using >trivia <cat | categories>.\n" +
                "Difficulty can be set to easy, medium or hard\n" +
                "Type is the question type (boolean: true/false, multiple: multiple choices)\n" +
                "Mode can be either time attack (first one getting the right answer wins) or turn by turn\n"
            )
            return

        cat_url = "https://opentdb.com/api_category.php"
        cat_json = requests.get(url=cat_url)
        categories = json.loads(cat_json.text)['trivia_categories']
        question_url = "https://opentdb.com/api.php?amount="
        game_players = {}

        if args[0] == "cat" or args[0] == "categories":
            display_cat = "Triva categories are: \n"
            for cat in categories:
                display_cat += (str(cat['id']) + ") " + cat['name'] + ".\n")
            await self.bot.say(display_cat)
            return
        argsnbr = len(args)
        j = 2
        # checking each argument so we don't have to put them in order // or have some left to random
        if args[0] == "new" and argsnbr >= 2:
            self.questions_nb = args[1]
            while j < argsnbr:
                if args[j].lower() in ["easy", "medium", "hard"]:
                    self.difficulty = args[j].lower()
                    j += 1
                    continue
                if args[j].lower() in ["boolean", "multiple"]:
                    self.type = args[j].lower()
                    j += 1
                    continue
                if int(args[j]) in range(categories[0]['id'], categories[len(categories) - 1]['id'] + 1):
                    self.category = args[j]
                    j += 1

        param = {'amount': self.questions_nb,
                 'category': self.category,
                 'difficulty': self.difficulty,
                 'type': self.type
                 }
        questions_json = requests.get(url=question_url, params=param)
        questions = json.loads(questions_json.text)['results']
        # i is the current question number
        i = 1
        # looping for each question
        for question in questions:
            answers_list = question['incorrect_answers']
            answers_list.append(question['correct_answer'])
            random.shuffle(answers_list)
            if question['type'] == "multiple":
                answers = "1) {}\n2) {}\n3) {}\n4) {}".format(answers_list[0], answers_list[1],
                                                              answers_list[2], answers_list[3])
            else:
                answers = '\n'.join(answers_list)
            embed = discord.Embed(colour=0x4C4CFF)
            embed.add_field(name="Question n°", value="{}/{}".format(i, self.questions_nb))
            embed.add_field(name="Category:", value=html.unescape(question['category']))
            embed.add_field(name="Question: ", value="**{}**".format(html.unescape(question['question'])))
            embed.add_field(name="Possible answers: ", value=html.unescape(answers), inline=False)
            await self.bot.say(embed=embed)
            i += 1

            if question['type'] == "boolean":
                player_answer = await self.bot.wait_for_message(channel=ctx.message.channel)
                while player_answer.content.lower() != question['correct_answer'].lower():
                    player_answer = await self.bot.wait_for_message(channel=ctx.message.channel)

            else:
                k = 0
                # finds where the correct answer is
                for k in range(0, 4):
                    if answers_list[k] == question['correct_answer']:
                        break
                player_answer = await self.bot.wait_for_message(channel=ctx.message.channel, content=str(k + 1))

            # goes out of the loop only if we get a correct answer
            # scoreboard - uses a dictionary, creates the key if it doesn't exists or adds one point.
            await self.bot.say("Correct! " + player_answer.author.mention + " scored a point!")
            if str(player_answer.author) in game_players.keys():
                game_players[str(player_answer.author)] += 1
            else:
                game_players[str(player_answer.author)] = 1

        scoreboard = discord.Embed(colour=0x4C4CFF)
        score = ""
        for player in sorted(game_players, key=game_players.get, reverse=True):
            score += "**{}**".format(player) + " with **{}** point(s)!\n".format(game_players[player])
        scoreboard.add_field(name="Scoreboard", value=score, inline=False)

        await self.bot.say("No more questions left! Here's the scoreboard for this game:")
        await self.bot.say(embed=scoreboard)
