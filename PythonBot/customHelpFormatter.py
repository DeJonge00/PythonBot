import asyncio, discord
from discord.ext import commands

class customHelpFormatter(commands.HelpFormatter):
    def __init__(self):
        super(customHelpFormatter, self).__init__()