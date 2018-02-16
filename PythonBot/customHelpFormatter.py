import asyncio, discord
from discord.ext import commands
import constants

class customHelpFormatter(commands.HelpFormatter):
    def __init__(self):
        super(customHelpFormatter, self).__init__()

    def format(self):
        return super().format()

    def get_ending_note(self):
        return "Message responses:\n\t'\\o/' : Praise the sun!\t'ded' (After a period of no messages) : Cry about a ded chat\t'(╯°□°）╯︵ ┻━┻' : '┬─┬ ノ( ゜-゜ノ)'\tMention me or 'biri' or 'biribiri' : I will talk to your lonely self\n" + super().get_ending_note() + "\nFor more questions use '{}helpserver' or message user 'Nya#2698'".format(constants.prefix)