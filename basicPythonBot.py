import asyncio, discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = Bot(command_prefix=commands.when_mentioned_or(">"), pm_help=1)

@bot.event
async def on_ready():
    print('Started bot')
	
# {prefix}echo <words>
@commands.command(pass_context=1, help="I'll be a parrot!")
async def echo(self, ctx, *args):
	return await self.bot.say(" ".join(args))
	
# Actually run the bot
bot.run(constants.bot_token)