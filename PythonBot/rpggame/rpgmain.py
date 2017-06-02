import asyncio, datetime, discord, log
from discord.ext import commands
from discord.ext.commands import Bot

# Normal commands
class RPGgame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bot.loop.create_task(self.gameloop())

    async def gameloop(self):
        await self.bot.wait_until_ready()
        #print("Gameloop started!")
        running = True;
        while running:
            time = datetime.datetime.utcnow()
            if time.minute%5 == 0:
                print(time)
            endtime = datetime.datetime.utcnow()
            #print(60-(endtime).seconds)
            await asyncio.sleep(60-endtime.second)

    # {prefix}battle <user>
    @commands.command(pass_context=1, help="Battle a fellow discord ally to a friendly brawl!")
    async def battle(self, ctx, *args):
        try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server.name + " | No permission to delete messages")

        except Exception as e:
            await log.error("cmd battle: " + str(e))