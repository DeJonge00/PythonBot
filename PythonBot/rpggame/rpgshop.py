import asyncio, constants, discord, removeMessage, math
from rpggame import rpgcharacter as rpgchar, rpgshopitem as rpgsi, rpgweapon as rpgw, rpgconstants as rpgc, rpgtrainingitem as rpgti
from discord.ext import commands
from discord.ext.commands import Bot

moneysign = "$"
SHOP_EMBED_COLOR = 0x00969b

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
            for i in rpgc.shopitems.values():
                embed.add_field(name=i.name, value="Costs: {}{}\nBenefits: {} {}".format(moneysign, i.cost, i.benefit, i.name))
            embed.add_field(name="Weapons", value="Type '{}shop weapon' for a list of available weapons".format(constants.prefix), inline=False)
            await self.bot.say(embed=embed)

    # {prefix}shop armor
    @shop.command(pass_context=1, aliases=["a", "armour"], help="Buy a shiny new suit of armor!")
    async def armor(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Blacksmith's Armory", icon_url=ctx.message.author.avatar_url)
            for i in sorted(rpgc.armor.values(), key=lambda x: x.cost):
                t = "Costs: {}{}".format(moneysign, i.cost)
                t += "\nDamage multiplier: *{}".format(i.absorption)
                t += "\nElement: {}".format(rpgc.elementnames.get(i.element))
                embed.add_field(name=i.name, value=t)
            await self.bot.say(embed=embed)
            return
        armor = rpgc.armor.get(" ".join(args).lower())
        if armor == None:
            await self.bot.say("That is not an armor sold in this part of the country")
            return
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if not player.buyArmor(armor):
            await self.bot.say("You do not have the money to buy the {}".format(armor.name))
            return
        await self.bot.say("You have acquired the {} for {}{}".format(armor.name, moneysign, armor.cost))

    # {prefix}shop critical
    @shop.command(pass_context=1, aliases=["c", "crit"], help="Special knowledge on enemy weakpoints")
    async def critical(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        try:
            a = int(args[0])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        if a < 0:
            await self.bot.say("Lmao, that sounds intelligent")
            return
        item = rpgc.shopitems.get("critical")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.critical += a*item.benefit
            await self.bot.say("{} bought {} critical knowledge for {}{}".format(ctx.message.author.mention, a, moneysign, a*item.cost))
        else:
            await self.bot.say("{} does not have enough money to buy {} critical knowledge\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

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
        item = rpgc.shopitems.get("damage")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.damage += a*item.benefit
            await self.bot.say("{} bought {} weapon sharpeners for {}{}".format(ctx.message.author.mention, a, moneysign, a*item.cost))
        else:
            await self.bot.say("{} does not have enough money to buy {} weapon sharpeners\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

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
        item = rpgc.shopitems.get("health")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addHealth(a*item.benefit)
            await self.bot.say("{} bought {} healthpotions for {}{}".format(ctx.message.author.mention, a, moneysign, a*item.cost))
        else:
            await self.bot.say("{} does not have enough money to buy {} healthpotions\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

    # {prefix}shop plates
    @shop.command(pass_context=1, aliases=["p"], help="Buy some armorplates")
    async def plates(self, ctx, *args):
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
        item = rpgc.shopitems.get("plates")
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if self.buyItem(player, item, amount=a):
            player.addArmor(a*item.benefit)
            await self.bot.say("{} bought {} plates of armor".format(ctx.message.author.mention, a))
        else:
            await self.bot.say("{} does not have enough money to buy {} armorplates\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, math.floor(player.money/item.cost)))

    # {prefix}shop weapon
    @shop.command(pass_context=1, aliases=["w", "weapons"], help="Buy a shiny new weapon!")
    async def weapon(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Shop Weapons", icon_url=ctx.message.author.avatar_url)
            for i in sorted(rpgc.weapons.values(), key=lambda x: x.cost):
                t = "Costs: {}{}".format(moneysign, i.cost)
                for e in i.effect:
                    x = i.effect.get(e)
                    t += "\n{}{}{}".format(e, x[0], x[1])
                t += "\nElement: {}".format(rpgc.elementnames.get(i.element))
                embed.add_field(name=i.name, value=t)
            await self.bot.say(embed=embed)
            return
        weapon = rpgc.weapons.get(" ".join(args).lower())
        if weapon == None:
            await self.bot.say("That is not a weapon sold in this part of the country")
            return
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if not player.buyWeapon(weapon):
            await self.bot.say("You do not have the money to buy the {}".format(weapon.name))
            return
        await self.bot.say("You have acquired the {} for {}{}".format(weapon.name, moneysign, weapon.cost))

    # {prefix}train
    @commands.group(pass_context=1, help="Train your skills!")
    async def train(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Available Training", icon_url=ctx.message.author.avatar_url)
            for i in rpgc.trainingitems.values():
                embed.add_field(name=i.name, value="Minutes per statpoint: {}".format(i.time))
            await self.bot.say(embed=embed)

    # {prefix}train hp
    @train.command(pass_context=1, aliases=["h", "health"], help="Train your character's health!")
    async def hp(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if player.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
        else:
            try:
                a = int(args[0])
            except ValueError:
                a = rpgchar.mintrainingtime
            except IndexError:
                a = rpgchar.mintrainingtime
            if player.busydescription != rpgchar.NONE:
                await self.bot.say("Please make sure you finish your other shit first")
                return
            item = rpgc.trainingitems.get("health")
            if not player.setBusy(rpgchar.TRAINING, a*item.time, ctx.message.channel.id):
                await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.maxtrainingtime))
                return
            player.raiseMaxhealth(a)
            await self.bot.say("{}, you are now training your health for {} minutes".format(ctx.message.author.mention, int(math.ceil(a*item.time))))

    # {prefix}train ws
    @train.command(pass_context=1, aliases=["w", "weaponskill"], help="Train your character's weaponskill, {} minutes per skillpoint!".format(10))
    async def ws(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        player = self.bot.rpggame.getPlayerData(ctx.message.author, ctx.message.author.display_name)
        if player.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
        else:
            try:
                a = int(args[0])
            except ValueError:
                a = 1
            except IndexError:
                a = 1
            if player.busydescription != rpgchar.NONE:
                await self.bot.say("Thou shalt not be busy when initiating a training session")
                return
            item = rpgc.trainingitems.get("weaponskill")
            if not player.setBusy(rpgchar.TRAINING, a*item.time, ctx.message.channel.id):
                await self.bot.say("You can train between {} and {} minutes".format(rpgchar.mintrainingtime, rpgchar.maxtrainingtime))
                return
            player.weaponskill += a
            await self.bot.say("{}, you are now training your weaponskill for {} minutes".format(ctx.message.author.mention, int(math.ceil(a*item.time))))
