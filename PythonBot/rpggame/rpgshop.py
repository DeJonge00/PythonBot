import asyncio, constants, discord, removeMessage, math
from rpggame import rpgcharacter as rpgchar, rpgshopitem as rpgsi, rpgweapon as rpgw
from discord.ext import commands
from discord.ext.commands import Bot

moneysign = "$"
SHOP_EMBED_COLOR = 0x00969b

shopitems = {"armor" : rpgsi.RPGShopItem("armor", 200, 10), "health" : rpgsi.RPGShopItem("health", 100, 10), "damage" : rpgsi.RPGShopItem("damage", 150, 5)}
weapons = {"Training sword" : rpgw.RPGWeapon("training sword", 0, {}), 
           "Axe" : rpgw.RPGWeapon("axe", 500, {"damage" : 1.1})}

class RPGShop:
    def __init__(self, bot):
        self.bot = bot

    def buyItem(self, player : rpgchar.RPGPlayer, item : rpgsi.RPGShopItem, amount = 1):
        if player.addMoney(-amount * item.cost):
            return True
        return False

    # {prefix}shop
    @commands.group(pass_context=1, help="Shop for valuable items!")
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Shop inventory", icon_url=ctx.message.author.avatar_url)
            for i in shopitems.values():
                embed.add_field(name=i.name, value="Costs: {}{}\nBenefits: {} {}".format(moneysign, i.cost, i.benefit, i.name))
            await self.bot.say(embed=embed)

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
        item = shopitems.get("armor")
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
        item = shopitems.get("health")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addHealth(a*item.benefit)
            await self.bot.say("{} bought {} healthpotions for {}{}".format(ctx.message.author.mention, a, moneysign, a*item.cost))
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
        item = shopitems.get("damage")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.damage += item.benefit
            await self.bot.say("{} bought {} weapon sharpeners for {}{}".format(ctx.message.author.mention, a, moneysign, a*item.cost))
        else:
            await self.bot.say("{} does not have enough money to buy {} healthpotions\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

    # {prefix}shop weapon
    @shop.command(pass_context=1, aliases=["w"], help="Buy a shiny new weapon!")
    async def damage(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            m = "**Weapons for sale:**"
            m += "\n".join(weapons.keys())
            await self.bot.say(m)
            return
        weapon = weapons.get(" ".join(args))
        if weapon == None:
            await self.bot.say("That is not a weapon sold in this part of the country")
            return
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if not self.buyWeapon(player, weapon):
            await self.bot.say("You do not have the money to buy the {}".format(weapon.name))
            return
        player.weapon = weapon
        await self.bot.say("You have acquired the {} for {}{}".format(weapon.name, moneysign, weapon.cost))

    # {prefix}train
    @commands.group(pass_context=1, help="Train your skills!")
    async def train(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Type '{}help train' for the list of available training sessions".format(constants.prefix))

    # {prefix}train hp
    @train.command(pass_context=1, aliases=["h", "health"], help="Train your character's health!")
    async def hp(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = rpgchar.mintrainingtime
        except IndexError:
            a = rpgchar.mintrainingtime
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if player.busydescription != rpgchar.NONE:
            await self.bot.say("Please make sure you finish your other shit first")
            return
        if not player.setBusy(rpgchar.TRAINING, a, ctx.message.channel.id):
            await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.maxtrainingtime))
            return
        player.raiseMaxhealth(a)
        await self.bot.say("{}, you are now training your health for {} minutes".format(ctx.message.author.mention, a))

    # {prefix}train ws
    @train.command(pass_context=1, aliases=["w", "weaponskill"], help="Train your character's weaponskill, {} minutes per skillpoint!".format(10))
    async def ws(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if player.busydescription != rpgchar.NONE:
            await self.bot.say("Thou shalt not be busy when initiating a training session")
            return
        if not player.setBusy(rpgchar.TRAINING, a*10, ctx.message.channel.id):
            await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.maxtrainingtime))
            return
        player.weaponskill += a
        await self.bot.say("{}, you are now training your weaponskill for {} minutes".format(ctx.message.author.mention, a*10))
