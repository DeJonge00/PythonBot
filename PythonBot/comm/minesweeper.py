import discord, log
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint

# Normal commands
class Minesweeper:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.running = False
    
    # {prefix}minesweeper
    @commands.command(pass_context=1, help="Minesweeper game", aliases=["ms"])
    async def minesweeper(self, ctx, *args):
        #try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")

            if len(args) <= 0:
                return await self.bot.send_message(ctx.message.channel, "Specify <new> | <x> <y>")
            if (not self.running):
                if not args[0] == "new":
                    return await self.bot.send_message(ctx.message.channel, "There is no game running right now. Try: >minesweeper new")
                self.height = 10
                self.width = 15
                self.mineamount = 20
                await self.initboard()
                return await self.sendboard(ctx.message.channel)
                
            
        #except Exception as e:
            #await log.error("cmd minesweeper: " + str(e))

    async def initboard(self):
        self.board = [[-1 for x in range(self.width)] for y in range(self.height)]
        self.mines = []
        for m in range(self.mineamount):
            while True:
                x = randint(0, self.height-1)
                y = randint(0, self.width-1)
                if not ((x, y) in self.mines):
                    break
            self.board[x][y] = 10
     
    async def sendboard(self, channel):
        m = "Mines left: " + str(len(self.mines)) + "\n    "
        for y in range(self.width):
            m += str(y) + " "
        for x in range(self.height):
            m += "\n" + str(x) + " "
            for y in range(self.width):
                if self.board[x][y] == -1:
                    m += "0 "
                if self.board[x][y] == 10:
                    m += "X "
        await self.bot.send_message(channel, m)