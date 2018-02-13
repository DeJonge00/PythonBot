import asyncio, removeMessage, math, constants
from rpggame import rpgcharacter as rpgchar, rpgshopitem as rpgsi
from discord.ext import commands
from discord.ext.commands import Bot

class RPGShop:
    def __init__(self, bot):
        self.bot = bot
        self.shopitems = {"armor" : rpgsi.RPGShopItem("armor", 200, 10), "health" : rpgsi.RPGShopItem("health", 100, 10), "damage" : rpgsi.RPGShopItem("damage", 150, 1.2)}

    def buyItem(self, player : rpgchar.RPGPlayer, item : rpgsi.RPGShopItem, amount = 1):
        if player.addMoney(-amount * item.cost):
            return True
        return False

    # {prefix}shop
    @commands.group(pass_context=1, help="Shop for valuable items!")
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Type '{}help shop' for the list of available items".format(constants.prefix))

    # {prefix}shop armor
    @shop.command(pass_context=1, aliases=["a", "ar", "armour"], help="Buy some armorplates")
    async def armor(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        if a < 0:
            await self.bot.say("You cannot sell your armor")
            return
        item = self.shopitems.get("armor")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addArmor(a*item.benefit)
            await self.bot.say("{} bought {} plates of armor".format(ctx.message.author.mention, a))
        else:
            await self.bot.say("{} does not have enough money to buy {} armorplates\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

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
        if a < 0:
            await self.bot.say("You cannot sacrifice blood *yet*")
            return
        item = self.shopitems.get("health")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addHealth(a*item.benefit)
            await self.bot.say("{} bought {} healthpotions".format(ctx.message.author.mention, a))
        else:
            await self.bot.say("{} does not have enough money to buy {} healthpotions\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

    # {prefix}shop damage
    @shop.command(pass_context=1, aliases=["d", "dam"], help="Buy a weapon upgrade")
    async def damage(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        if a < 0:
            await self.bot.say("It would be unwise to blunten your weapon")
            return
        item = self.shopitems.get("damage")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.damage = int(math.floor(player.damage * math.pow(item.benefit, a)))
            await self.bot.say("{} bought {} weapon sharpeners".format(ctx.message.author.mention, a))
        else:
            await self.bot.say("{} does not have enough money to buy {} healthpotions\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

    # {prefix}train
    @commands.group(pass_context=1, help="Train your skills!")
    async def train(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Type '{}help train' for the list of available training sessions".format(constants.prefix))

    # {prefix}train hp
    @train.command(pass_context=1, aliases=["h", "hp"], help="Train your character's health!")
    async def health(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = rpgchar.mintrainingtime
        except IndexError:
            a = rpgchar.mintrainingtime
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if not player.setBusy(rpgchar.TRAINING, time, ctx.message.channel.id):
            await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.mintrainingtime))
            return
        player.raiseMaxhealth(a)
        await self.bot.say("{}, you are now training your health for {} minutes".format(ctx.message.author.mention, time))

    # {prefix}train ws
    @train.command(pass_context=1, aliases=["w", "ws"], help="Train your character's weaponskill, {} minutes per skillpoint!".format(10))
    async def weaponskill(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if not player.setBusy(rpgchar.TRAINING, a*10, ctx.message.channel.id):
            await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.mintrainingtime))
            return
        player.weaponskill += a
        await self.bot.say("{}, you are now training your weaponskill for {} minutes".format(ctx.message.author.mention, time))
