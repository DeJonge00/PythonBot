import asyncio, removeMessage, math
import rpggame.rpgcharacter as rpgchar, rpggame.rpgshopitem as rpgsi
from discord.ext import commands
from discord.ext.commands import Bot

class RPGShop:
    def __init__(self, bot):
        self.bot = bot
        self.items = {"health" : rpgsi.RPGShopItem("health", 100), "damage" : rpgsi.RPGShopItem("damage", 150)}

    def __str__(self):
        inventory = "**Shop inventory**"
        for item in self.items.values():
            inventory += "\n" + item.name + ", $" + str(item.cost)
        return inventory + "\n\nHappy adventuring!"

    def buyItem(self, player : rpgchar.RPGPlayer, item : rpgsi.RPGShopItem, amount = 1):
        if player.addMoney(-amount * item.getCost()):
            return True
        return False

    @commands.group(pass_context=1, aliases=["s"], help="Shop for valuable items!")
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say(str(self))

    # {prefix}shop health
    @shop.command(pass_context=1, aliases=["h", "hp"], help="Buy a healthpotion")
    async def health(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        item = self.items.get("health")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addHealth(a*10)
            await self.bot.say(ctx.message.author.mention + " bought " + str(a) + " healthpotions")
        else:
            await self.bot.say(ctx.message.author.mention + " does not have enough money to buy " + str(a) + " healthpotions\nThe maximum you can afford is " + str(math.floor(player.money/item.cost)))