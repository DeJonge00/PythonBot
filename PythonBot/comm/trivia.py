import discord
import json
import html
import requests
import random
import asyncio

# this game has been made with the open trivia db API : https://opentdb.com/
# All data provided by the API is available under the Creative Commons Attribution-ShareAlike 4.0 International License.


class Trivia:
    """Init Trivia game with the number of questions, their category, difficulty and type (boolean or multiple)"""
    def __init__(self, my_bot, channel, author, categories, mode):
        self.bot = my_bot
        self.questions_nb = ""
        self.categories = categories
        self.category = ""
        self.difficulty = ""
        self.type = ""
        self.players = []
        self.mode = mode
        self.channel = channel
        self.game_creator = author
        self.joinable = False

    # setters
    def set_category(self, new_category):
        self.category = new_category

    def set_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty

    def set_type(self, new_type):
        self.type = new_type

    def set_mode(self, new_mode):
        self.mode = new_mode

    async def set_questions_nb(self, new_questions_nb):
        self.questions_nb = int(new_questions_nb)

    async def player_join(self, author):
        if not self.joinable:
            await self.bot.say(author.mention + " sorry but it's either too late or there's no game in preparation.")
            return
        for p in self.players:
            if author == p.playerid:
                await self.bot.say(author.mention + " you are already registered for this party, baka!")
                return
        self.players.append(TriviaPlayer(author))
        await self.bot.say(author.mention + " joins the battle!")

    async def player_quit(self, author):
        for player in self.players:
            if player.playerid == author:
                player.quit_game()
                await self.bot.say(player.playerid.mention + " left the game!")
                return
        await self.bot.say(author.mention + " you are currently not in any party on this channel.")

    async def allow_join(self):
        self.joinable = True
        await asyncio.sleep(60.0)
        self.joinable = False
        await self.bot.say("Game starting!")
        await self.set_questions_nb(self.questions_nb * len(self.players))
        await self.start_turns_game()

    async def get_params(self):
        def is_cat(msg):
            if msg.content.lower() == "any":
                return True
            if is_natural_nbr(msg.content) and \
                    int(msg.content) in range(self.categories[0]['id'],
                                              self.categories[len(self.categories) - 1]['id'] + 1):
                return True
            return False

        def is_dif(msg):
            return msg.content.lower() in ["easy", "medium", "hard", "any"]

        def is_type(msg):
            return msg.content.lower() in ["boolean", "multiple", "any"]

        # CATEGORIES
        await self.bot.say(
            "Specify a category number: (use '>trivia categories' to display categories) or type 'any' for random.")
        category = await self.bot.wait_for_message(channel=self.channel,
                                                   author=self.game_creator, check=is_cat, timeout=30.0)
        if category.content.lower() != "any":
            self.set_category(int(category.content))
        if await self.is_timeout(category):
            return

        # DIFFICULTY
        await self.bot.say(
            "Specify a difficulty: 'easy', 'medium', 'hard' or 'any'.")
        difficulty = await self.bot.wait_for_message(channel=self.channel,
                                                     author=self.game_creator, check=is_dif, timeout=30.0)
        if difficulty.content.lower() != "any":
            self.set_difficulty(difficulty.content)
        if await self.is_timeout(difficulty):
            return

        # QUESTION TYPE
        await self.bot.say("Specify a question type: 'boolean', 'multiple' or 'any'.")
        new_type = await self.bot.wait_for_message(channel=self.channel,
                                                   author=self.game_creator, check=is_type, timeout=30.0)
        if new_type.content.lower() != "any":
            self.set_type(new_type.content.lower())
        if await self.is_timeout(new_type):
            return

        # TURN MODE
        if self.mode == "turn":
            await self.bot.say("How many questions per players?")
            question_answer = await self.bot.wait_for_message(channel=self.channel,
                                                              author=self.game_creator, check=is_natural, timeout=30.0)
            if await self.is_timeout(question_answer):
                return
            await self.bot.say("Parameters completed! Each person that now wants to join the game has 60 "
                               "seconds to use >trivia join on this channel to participate to the upcoming game")
            await self.set_questions_nb(int(question_answer.content))
            await self.allow_join()

        # TIME MODE
        else:
            await self.bot.say("How many questions? (required)")
            question_answer = await self.bot.wait_for_message(channel=self.channel,
                                                              author=self.game_creator, check=is_natural, timeout=30.0)
            if await self.is_timeout(question_answer):
                return
            await self.set_questions_nb(question_answer.content)

    def init_game(self):
        question_url = "https://opentdb.com/api.php"
        questions_numb = int(self.questions_nb)
        questions = []
        while questions_numb > 0:
            if questions_numb > 49:
                request_question = '49'
            else:
                request_question = str(questions_numb)
            param = {'amount': request_question,
                     'category': self.category,
                     'difficulty': self.difficulty,
                     'type': self.type}
            new_request = json.loads((requests.get(url=question_url, params=param)).text)['results']
            questions += new_request
            questions_numb -= 49

        return questions

    async def start_turns_game(self):
        questions = self.init_game()
        question_number = 1
        player_index = 0
        if len(self.players) < 1:
            await self.bot.say("No one joined the game, cancelling...")
            return
        for question in questions:
            # skip player turn and his question if he left the game
            if player_index >= len(self.players):
                player_index = 0
            if self.players[player_index].isplaying:
                await self.ask_question(self.players[player_index], question, question_number)
                question_number += 1
                player_index += 1
        await self.bot.say("Game is over! Here's the leaderboard:")
        await self.display_leaderboard()

    async def ask_question(self, player, question, question_nb):
        answers_list = question['incorrect_answers']
        answers_list.append(question['correct_answer'])
        random.shuffle(answers_list)
        if question['type'] == "multiple":
            answers = "1) {}\n2) {}\n3) {}\n4) {}".format(answers_list[0], answers_list[1],
                                                          answers_list[2], answers_list[3])
        else:
            answers = '\n'.join(answers_list)
        embed = discord.Embed(colour=0x4C4CFF)
        embed.add_field(name="Question n°", value="{}/{}".format(question_nb, self.questions_nb))
        embed.add_field(name="Category:", value=html.unescape(question['category']))
        embed.add_field(name="Question: ", value="**{}**".format(html.unescape(question['question'])))
        embed.add_field(name="Possible answers: ", value=html.unescape(answers), inline=False)
        await self.bot.say(player.playerid.mention + " this question is for you:")
        await self.bot.say(embed=embed)
        if question['type'] == "multiple":
            player_answer = await self.bot.wait_for_message(channel=self.channel,
                                                            author=player.playerid, check=is_acceptable_answer,
                                                            timeout=60.0)
        else:
            player_answer = await self.bot.wait_for_message(channel=self.channel, author=player.playerid, timeout=60.0)
        if player_answer is None:
            await self.bot.say("The question was apparently too complicated for " + player.playerid.mention)
            return
        if self.is_answer_correct(question, player_answer.content.lower(), answers_list):
            player.add_point()
            await self.bot.say(
                player.playerid.mention + " correct! You win 1 point. Current score: {}".format(player.score))
        else:
            await self.bot.say(player.playerid.mention + " wrong! The correct answer was: {}. Current score: {}".
                               format(html.unescape(question['correct_answer']), player.score))

    @staticmethod
    def is_answer_correct(question, answer, answers_list):
        if is_natural_nbr(answer):
            if answers_list[int(answer) - 1] == question['correct_answer']:
                return True
        if answer == question['correct_answer'].lower():
            return True
        return False

    async def display_leaderboard(self):
        embed = discord.Embed(colour=0x4C4CFF)
        p = 0
        long_ass_string = ""
        while p < 10 and p < len(self.players):
            long_ass_string += "{}: {} points.\n".format(self.players[p].playerid, self.players[p].score)
            p += 1
        embed.add_field(name="Trivia Leaderboard", value=long_ass_string)
        await self.bot.say(embed=embed)

    async def is_timeout(self, msg):
        if msg is None:
            await self.bot.say("game creation timed out :sob:")
            return True
        return False


def is_natural(msg):
    try:
        nbr = int(msg.content)
        return 0 < nbr < 6000
    except Exception:
        return False


def is_acceptable_answer(msg):
    try:
        nbr = int(msg.content)
        return 1 <= nbr <= 4
    except Exception:
        return False


def is_natural_nbr(msg):
    if msg.isdigit() and int(msg) > 0:
        return True
    return False


class TriviaPlayer:
    def __init__(self, playerid):
        self.playerid = playerid
        self.isplaying = True
        self.score = 0

    def add_point(self):
        self.score += 1

    def quit_game(self):
        self.isplaying = False




    # # {prefix}trivia <categories>
    # @commands.command(pass_context=1, help="Trivia", aliases=["tr"])
    # async def trivia(self, ctx, *args):
    #     if not await self.bot.pre_command(message=ctx.message, command="trivia"):
    #         return
    #     if len(args) <= 0:
    #         await self.bot.say("[Usage] To start a new game use: >trivia new <mode>('turns' or 'time')")
    #         return
    #     categories_url = "https://opentdb.com/api_category.php"
    #
    #
    #     if args[0] == "cat" or args[0] == "categories":
    #         await self.display_categories()
    #         return
    #
    #     if args[0] == "join":
    #         if not self.joinable:
    #             await self.bot.say(
    #                 self.game_creator.mention + " sorry but it's either too late or there's no game in preparation.")
    #             return
    #         for p in self.players:
    #             if self.game_creator == p.playerid:
    #                 await self.bot.say(self.game_creator.mention + " you are already registered for this party, baka!")
    #                 return
    #         self.player_join(self.game_creator)
    #         await self.bot.say(self.game_creator.mention + " joins the battle!")
    #
    #     if args[0] == "quit":
    #         for p in self.players:
    #             if p.playerid == self.game_creator:
    #                 self.players.remove(p)
    #                 return
    #         await self.bot.say(self.game_creator.mention + " you are not registered in a party!")
    #
    #     if args[0] == "new":
    #         await self.bot.say("New trivia game requested!\nPlease chose a game mode: 1)time attack  2)turn by turn")
    #         game_mode = await self.bot.wait_for_message(channel=self.channel, author=self.game_creator)
    #         if game_mode.content == '1':
    #             await self.bot.say("Time attack mode selected!")
    #             self.set_mode("time")
    #         elif game_mode.content == '2':
    #             await self.bot.say("Turn by turn mode selected!")
    #             self.set_mode("turn")
    #         else:
    #             await self.bot.say(self.game_creator.mention + " stop wasting my time.")
    #             return
    #         await self.get_params(ctx)
