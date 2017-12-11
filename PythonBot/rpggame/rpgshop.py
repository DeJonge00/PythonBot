import asyncio, rpggame.rpgcharacter, rpggame.rpgshopitem
from discord.ext import commands
from discord.ext.commands import Bot

class rpgshop:
    def __init__(self):
        self.items = [rpgshopitem("health", 100), rpgshopitem("damage", 150)]

    async def showShopInventory(self, ctx):
        inventory = ""
        for item in self.items:
            inventory += item.getName() + ", $" + item.getCost()
        return await self.bot.send_message(ctx.message.channel, inventory)

    async def buyItem(self, player : rpgplayer, item : rpgshopitem, amount = 1):
        if player.decreaseMoney(amount * item.getCost()):
            return True
        return False
