import asyncio, datetime, discord, log
from discord.ext import commands
from discord.ext.commands import Bot

# Normal commands
class RPGgame:
    def __init__(self, my_bot):
        self.bot = my_bot
        #gameloop()

async def gameloop():
    running = True
    while(running):
        time = datetime.datetime.utcnow()

        endtime = datetime.datetime.utcnow()
        print(endtime-time)
        asyncio.sleep(1)

# {prefix}battle <user>
    @commands.command(pass_context=1, help="Battle a fellow discord ally to a friendly brawl!")
    async def fps(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")

        except Exception as e:
            await log.error("cmd battle: " + str(e))