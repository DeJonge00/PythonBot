import discord, log
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
from PIL import Image

MINE = 10
UNGUESSED = -1

# Normal commands
class Minesweeper:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.running = False
        self.hasboard = False
    
    # {prefix}minesweeper
    @commands.command(pass_context=1, help="Minesweeper game", aliases=["ms"])
    async def minesweeper(self, ctx, *args):
        #try:
            try:
                await self.bot.delete_message(ctx.message)
            except discord.Forbidden:
                print(ctx.message.server + " | No permission to delete messages")

            if len(args) <= 0:
                return await self.bot.send_message(ctx.message.channel, "Specify 'new' {height} {width} {mines} | <x> <y> | 'quit'")
            if args[0] == "quit":
                return await self.quit(ctx.message.channel)
            if (not self.running):
                if not args[0] == "new":
                    return await self.bot.send_message(ctx.message.channel, "There is no game running right now. Try: >minesweeper new")
                if len(args) >= 4:
                    try:
                        self.height = int(args[1])
                    except ValueError:
                        self.height = 10
                    try:
                        self.width = int(args[2])
                    except ValueError:
                        self.width = 15
                    try:
                        self.mineamount = int(args[3])
                    except ValueError:
                        self.mineamount = 20
                    if (0 >= self.height) | (self.height > 30):
                        return await self.bot.send_message(ctx.message.channel, "The height can be between 0 and 30")
                    if (0 >= self.width) | (self.width > 30):
                        return await self.bot.send_message(ctx.message.channel, "The width can be between 0 and 30")
                    if (0 >= self.mineamount) | (self.mineamount > (self.height * self.width)):
                        return await self.bot.send_message(ctx.message.channel, "Wowowow, that difficulty is not something you could handle...")
                    if self.height > self.width:
                        self.width += self.height
                        self.height = self.width-self.height
                        self.width -= self.height
                else:
                    self.height = 10
                    self.width = 15
                    self.mineamount = 20
                self.running = True
                return await self.bot.send_message(ctx.message.channel, "Game initialized with a " + str(self.height) + "x" + str(self.width) + " board, glhf")
            else:
                # Running = True
                if len(args) > 0:
                    if args[0] == "flag":
                        if len(args) > 2:
                            try:
                                y = int(args[1])-1
                                x = int(args[2])-1
                            except ValueError:
                                return await self.bot.send_message(ctx.message.channel, "Those x or y values are not numbers...")
                            if (x <= 0) | (y <= 0) | (x >= self.height) | (y >= self.width):
                                return await self.bot.send_message(ctx.message.channel, "Those x or y values are not on the board")
                            self.image.paste(Image.open("./minesweeper/flag.jpg"), (20*y+10, 20*x+10))
                            return await self.sendboard(ctx.message.channel)
                        return await self.bot.send_message(ctx.message.channel, "Those x or y values are not even existent")
                    else: 
                        if len(args) < 2:
                            return await self.bot.send_message(ctx.message.channel, "Specify a tile to check (<x> <y>)")
                        try:
                            y = int(args[0])-1
                            x = int(args[1])-1
                        except ValueError:
                            return await self.bot.send_message(ctx.message.channel, "Those x or y values are not even numbers")
                        if (x < 0) | (y < 0) | (x >= self.height) | (y >= self.width):
                            return await self.bot.send_message(ctx.message.channel, "Those x or y values are not on the board")
                        await self.bot.send_message(ctx.message.channel, "You guessed: (" + str(y+1) + "," + str(x+1) + "):")
                        if not await self.guess(x, y):
                            await self.bot.send_message(ctx.message.channel, "DEAD Hahaha (your score was: " + str(self.score) + "/" + str(self.width * self.height - self.mineamount) +  ")")
                            return await self.sendboard(ctx.message.channel)
            return await self.sendboard(ctx.message.channel)
        #except Exception as e:
            #await log.error("cmd minesweeper: " + str(e))

    async def gameover(self):
        self.hasboard = False
        self.running = False

    # Return isdead (True | False)
    async def guess(self, x, y):
        if not self.hasboard:
            await self.initboard(x, y)
        if self.board[x][y] == MINE:
            for a in range(0, self.height):
                for b in range(0, self.width):
                    self.image.paste(Image.open("./minesweeper/" + str(self.board[a][b]) + ".jpg"), (20*b+10, 20*a+10))
            await self.gameover()
            return False
        if self.board[x][y] == UNGUESSED:
            self.score += 1
        n = 0
        for h in range(max(0, x-1), min(x+2, self.height)):
            for w in range(max(0, y-1), min(y+2, self.width)):
                if (h != x) | (w != y):
                    if self.board[h][w] == MINE:
                        n += 1
        self.board[x][y] = n
        self.image.paste(Image.open("./minesweeper/" + str(n) + ".jpg"), (20*y+10, 20*x+10))
        if n == 0:
            for h in range(max(0, x-1), min(x+2, self.height)):
                for w in range(max(0, y-1), min(y+2, self.width)):
                    if ((h != x) | (w != y)) & (self.board[h][w] == UNGUESSED):
                        await self.guess(h, w)
        return True

    async def initboard(self, h, w):
        self.board = [[UNGUESSED for x in range(self.width)] for y in range(self.height)]
        self.mines = [(h,w)]
        for m in range(self.mineamount):
            while True:
                x = randint(0, self.height-1)
                y = randint(0, self.width-1)
                if ((x, y) not in self.mines):
                    break
            self.mines += (x, y)
            self.board[x][y] = MINE
        self.score = 0
        self.image = Image.new("RGB", (20+(20*self.width),20+(20*self.height)), "white")
        empty = Image.open("./minesweeper/-1.jpg")
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.image.paste(empty, (20*x+10, 20*y+10))
        self.hasboard = True
     
    async def sendboard(self, channel):
        if self.score >= ((self.width * self.height) - self.mineamount):
            await self.gameover()
            await self.bot.send_message(channel, "You win, congratulations!!")
        """
        m = "Mines left: " + str(len(self.mines)) + "\n    "
        for y in range(self.width):
            m += str(y) + " "
        for x in range(self.height):
            m += "\n" + str(x) + " "
            for y in range(self.width):
                if (self.board[x][y] == UNGUESSED) | (self.board[x][y] == MINE):
                    m += "? "
                else:
                    m += str(self.board[x][y]) + " "
        await self.bot.send_message(channel, m)
        """
        self.image.save("./minesweeper/state.png")
        await self.bot.send_file(channel, "./minesweeper/state.png")

    async def quit(self, channel):
        self.running = False
        await self.bot.send_message(channel, "The game has been aborted")