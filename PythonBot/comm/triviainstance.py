import discord
import json
import html
import requests
import random
import asyncio

# this game has been made with the open trivia db API : https://opentdb.com/
# All data provided by the API is available under the Creative Commons Attribution-ShareAlike 4.0 International License.


class TriviaInstance:
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
        self.keep_playing = True

    def set_category(self, new_category):
        self.category = new_category

    def set_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty

    def set_type(self, new_type):
        self.type = new_type

    def set_mode(self, new_mode):
        self.mode = new_mode

    def stop_playing(self):
        self.keep_playing = False

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
            # duplicates are not handled
            new_request = json.loads((requests.get(url=question_url, params=param)).text)['results']
            questions += new_request
            questions_numb -= 49

        return questions

    def is_player_registered(self, player):
        for p in self.players:
            if player == p.playerid:
                return p
        return False

    async def player_turn_join(self, author):
        if not self.joinable:
            await self.bot.say(author.mention + " sorry but it's either too late or there's no game in preparation.")
            return
        if self.is_player_registered(author):
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

    async def set_questions_nb(self, new_questions_nb):
        self.questions_nb = int(new_questions_nb)

    async def get_params(self, ctx):
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

        prefix = await self.bot._get_prefix(ctx.message)
        # CATEGORIES
        await self.bot.say(
            "Specify a category number: (use '{}trivia categories' to display categories) or"
            " type 'any' for random.".format(prefix))
        category = await self.bot.wait_for_message(channel=self.channel,
                                                   author=self.game_creator, check=is_cat, timeout=30.0)
        if await self.is_timeout(category):
            return
        if category.content.lower() != "any":
            self.set_category(int(category.content))

        # DIFFICULTY
        await self.bot.say(
            "Specify a difficulty: 'easy', 'medium', 'hard' or 'any'.")
        difficulty = await self.bot.wait_for_message(channel=self.channel,
                                                     author=self.game_creator, check=is_dif, timeout=30.0)
        if await self.is_timeout(difficulty):
            return
        if difficulty.content.lower() != "any":
            self.set_difficulty(difficulty.content)

        # QUESTION TYPE
        await self.bot.say("Specify a question type: 'boolean', 'multiple' or 'any'.")
        new_type = await self.bot.wait_for_message(channel=self.channel,
                                                   author=self.game_creator, check=is_type, timeout=30.0)
        if await self.is_timeout(new_type):
            return
        if new_type.content.lower() != "any":
            self.set_type(new_type.content.lower())

        # TURN MODE
        if self.mode == "turn":
            await self.bot.say("How many questions per players?")
            question_answer = await self.bot.wait_for_message(channel=self.channel,
                                                              author=self.game_creator, check=is_natural, timeout=30.0)
            if await self.is_timeout(question_answer):
                return
            await self.bot.say("Parameters completed! Each person that now wants to join the game has 60 "
                               "seconds to use {}trivia join on this channel "
                               "to participate to the upcoming game".format(prefix))
            await self.set_questions_nb(int(question_answer.content))
            await self.allow_join()

        # TIME MODE
        else:
            await self.bot.say("How many questions?")
            question_answer = await self.bot.wait_for_message(channel=self.channel,
                                                              author=self.game_creator, check=is_natural, timeout=30.0)
            if await self.is_timeout(question_answer):
                return
            await self.set_questions_nb(question_answer.content)
            await self.stat_time_game()

    async def start_turns_game(self):
        questions = self.init_game()
        question_number = 1
        player_index = 0
        if len(self.players) < 1:
            await self.bot.say("No one joined the game, cancelling...")
            return
        for question in questions:
            if not self.keep_playing:
                await self.bot.say("Game cancelled by {}.".format(self.game_creator.mention))
                return
            # skip player turn and his question if he left the game
            if player_index >= len(self.players):
                player_index = 0
            if self.players[player_index].isplaying:
                await self.ask_target_question(self.players[player_index], question, question_number)
            player_index += 1
            question_number += 1
        await self.bot.say("Game is over! Here's the leaderboard:")
        await self.display_leaderboard()

    async def stat_time_game(self):
        await self.bot.say("In this mode, the first one that answers correctly wins a point but each player"
                           " has only one try per question, be careful!")
        questions = self.init_game()
        question_nb = 1
        for question in questions:
            if not self.keep_playing:
                await self.bot.say("Game cancelled by {}.".format(self.game_creator.mention))
                return
            failed_players = []
            answers_list = question['incorrect_answers']
            answers_list.append(question['correct_answer'])
            random.shuffle(answers_list)
            if question['type'] == "multiple":
                answers = "1) {}\n2) {}\n3) {}\n4) {}".format(answers_list[0], answers_list[1],
                                                              answers_list[2], answers_list[3])
            else:
                answers = '\n'.join(answers_list)
            await self.display_question(question, question_nb, answers)
            if question['type'] == "multiple":
                def is_correct_multiple_answer(msg):
                    if msg.author in failed_players:
                        return False
                    failed_players.append(msg.author)
                    if is_acceptable_answer(msg) and self.is_answer_correct(question, msg.content, answers_list):
                        return True
                    return False

                player_answer = await self.bot.wait_for_message(channel=self.channel, check=is_correct_multiple_answer,
                                                                timeout=60.0)
            else:
                def is_correct_boolean_answer(msg):
                    if msg.author in failed_players:
                        return False
                    failed_players.append(msg.author)
                    if is_boolean_answer(msg) and msg.content.lower() == question['correct_answer'].lower():
                        return True
                    return False

                player_answer = await self.bot.wait_for_message(channel=self.channel,
                                                                check=is_correct_boolean_answer, timeout=60.0)
            if player_answer is None:
                await self.bot.say("Looks like everyone was scared to answer that question")
                question_nb += 1
                continue

            await self.bot.say("Correct! " + player_answer.author.mention + " wins 1 point!")
            player = self.is_player_registered(player_answer.author)
            if not player:
                self.players.append(TriviaPlayer(player_answer.author))
                self.players[len(self.players) - 1].add_point()
            else:
                player.add_point()
            question_nb += 1
        await self.bot.say("Game is over! Here's the leaderboard:")
        await self.display_leaderboard()

    async def display_question(self, question , question_nb, answers):
        embed = discord.Embed(colour=0x4C4CFF)
        embed.add_field(name="Question n°", value="{}/{}".format(question_nb, self.questions_nb))
        embed.add_field(name="Category:", value=html.unescape(question['category']))
        embed.add_field(name="Question: ", value="**{}**".format(html.unescape(question['question'])))
        embed.add_field(name="Possible answers: ", value=html.unescape(answers), inline=False)
        await self.bot.say(embed=embed)

    async def ask_target_question(self, player, question, question_nb):
        def is_multiple_acceptable(msg):
            return is_acceptable_answer(msg) and player.isplaying

        def is_boolean_acceptable(msg):
            return is_boolean_answer(msg) and player.isplaying

        answers_list = question['incorrect_answers']
        answers_list.append(question['correct_answer'])
        random.shuffle(answers_list)
        if question['type'] == "multiple":
            answers = "1) {}\n2) {}\n3) {}\n4) {}".format(answers_list[0], answers_list[1],
                                                          answers_list[2], answers_list[3])
        else:
            answers = '\n'.join(answers_list)
        await self.bot.say(player.playerid.mention + " this question is for you:")
        await self.display_question(question, question_nb, answers)
        if question['type'] == "multiple":
            player_answer = await self.bot.wait_for_message(channel=self.channel,
                                                            author=player.playerid, check=is_multiple_acceptable,
                                                            timeout=60.0)
        else:
            player_answer = await self.bot.wait_for_message(channel=self.channel, author=player.playerid,
                                                            check=is_boolean_acceptable, timeout=60.0)
        if player_answer is None:
            await self.bot.say("The question was apparently too complicated.")
            return
        if self.is_answer_correct(question, player_answer.content.lower(), answers_list):
            player.add_point()
            await self.bot.say(
                player.playerid.mention + " correct! You win 1 point. Current score: {}".format(player.score))
        else:
            await self.bot.say(player.playerid.mention + " wrong! The correct answer was: {}. Current score: {}".
                               format(html.unescape(question['correct_answer']), player.score))

    async def display_leaderboard(self):
        embed = discord.Embed(colour=0x4C4CFF)
        p = 0
        long_ass_string = ""
        if len(self.players) > 0:
            self.players.sort(key=lambda x: x.score, reverse=True)
            while p < 10 and p < len(self.players):
                plural = ""
                if self.players[p].score > 1:
                    plural = "s"
                long_ass_string += "{}: {} point{}.\n".format(self.players[p].playerid, self.players[p].score, plural)
                p += 1
            embed.add_field(name="Trivia Leaderboard", value=long_ass_string)
            await self.bot.say(embed=embed)

    async def is_timeout(self, msg):
        if msg is None:
            await self.bot.say("game creation timed out :sob:")
            return True
        return False

    @staticmethod
    def is_answer_correct(question, answer, answers_list):
        if is_natural_nbr(answer):
            if answers_list[int(answer) - 1] == question['correct_answer']:
                return True
        if answer == question['correct_answer'].lower():
            return True
        return False


def is_natural(msg):
    try:
        nbr = int(msg.content)
        return 0 < nbr < 1001
    except Exception:
        return False


def is_acceptable_answer(msg):
    try:
        nbr = int(msg.content)
        return 1 <= nbr <= 4
    except Exception:
        return False


def is_boolean_answer(msg):
    return msg.content.lower() in ["true", "false"]


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
