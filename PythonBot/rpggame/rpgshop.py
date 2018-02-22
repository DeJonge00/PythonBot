import asyncio, constants, discord, removeMessage, math
from rpggame import rpgcharacter as rpgchar, rpgshopitem as rpgsi, rpgconstants as rpgc, rpgtrainingitem as rpgti, rpgweapon as rpgw
from discord.ext import commands
from discord.ext.commands import Bot

moneysign = "$"
SHOP_EMBED_COLOR = 0x00969b

class RPGShop:
    def __init__(self, bot):
        self.bot = bot
        self.weapons = []

    def reloadShopWeapons(self):
        self.weapons = []
        for i in range(1,6):
            self.weapons.append(rpgw.generateWeapon(i*1000))

    # {prefix}shop
    @commands.group(pass_context=1, help="Shop for valuable items!")
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Shop commands", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Items", value="Type '{}shop item' for a list of available items".format(constants.prefix), inline=False)
            embed.add_field(name="Weapons", value="Type '{}shop weapon' for a list of available weapons".format(constants.prefix), inline=False)
            await self.bot.say(embed=embed)

    # {prefix}shop armor
    @shop.command(pass_context=1, aliases=["a", "armour"], help="Buy a shiny new suit of armor!")
    async def armor(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        player = self.bot.rpggame.getPlayerData(ctx.message.author.id, ctx.message.author.display_name)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.add_field(name="Your money", value="{}{}".format(moneysign, player.money))
            embed.set_author(name="Blacksmith's Armory", icon_url=ctx.message.author.avatar_url)
            for i in sorted(rpgc.armor.values(), key=lambda x: x.cost):
                t = "Costs: {}{}".format(moneysign, i.cost)
                abso = i.benefit.get("absorption")
                if abso != None:
                    t += "\nDamage multiplier: {}{}".format(abso[0], abso[1])
                t += "\nElement: {}".format(rpgc.elementnames.get(i.element))
                embed.add_field(name=i.name, value=t)
            await self.bot.say(embed=embed)
            return
        armor = rpgc.armor.get(" ".join(args).lower())
        if armor == None:
            await self.bot.say("That is not an armor sold in this part of the country")
            return
        if not player.buyArmor(armor):
            await self.bot.say("You do not have the money to buy the {}".format(armor.name))
            return
        await self.bot.say("You have acquired the {} for {}{}".format(armor.name, moneysign, armor.cost))

    # {prefix}shop item
    @shop.command(pass_context=1, aliases=["i", "buy"], help="Special knowledge on enemy weakpoints")
    async def item(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        player = self.bot.rpggame.getPlayerData(ctx.message.author.id, ctx.message.author.display_name)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Shop inventory", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Your money", value="{}{}".format(moneysign, player.money))
            for i in sorted(rpgc.shopitems.values(), key=lambda x: x.cost):
                t = "Costs: {}{}".format(moneysign, i.cost)
                t += "\nYou can afford {} of this item".format(math.floor(player.money/i.cost))
                for e in i.benefit:
                    x = i.benefit.get(e)
                    t += "\n{}{}{}".format(e, x[0], x[1])
                embed.add_field(name=i.name, value=t)
            await self.bot.say(embed=embed)
            return
        item = args[0].lower()
        if item in ["h", "hp"]:
            item = "health"
        elif item in ["d", "dam"]:
            item = "damage"
        elif item in ["a", "armour", "armorplates", "armor"]:
            item = "plates"
        elif item in ["c", "crit"]:
            item = "critical"
        item = rpgc.shopitems.get(item)
        if item==None:
            await self.bot.say("Thats not an item sold here")
            return
        try:
            a = int(args[1])
        except ValueError:
            a = 1
        except IndexError:
            a = 1
        if a < 0:
            await self.bot.say("Lmao, that sounds intelligent")
            return
        if player.buyItem(item, amount=a):
            await self.bot.say("{} bought {} {} for {}{}".format(ctx.message.author.mention, a, item.name, moneysign, a*item.cost))
        else:
            await self.bot.say("{} does not have enough money to buy {} {}\nThe maximum you can afford is {}".format(ctx.message.author.mention, a, item.name, math.floor(player.money/item.cost)))

    # {prefix}shop weapon
    @shop.command(pass_context=1, aliases=["w", "weapons"], help="Buy a shiny new weapon!")
    async def weapon(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        player = self.bot.rpggame.getPlayerData(ctx.message.author.id, ctx.message.author.display_name)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Shop Weapons", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Your money", value="{}{}".format(moneysign, player.money))
            for i in self.weapons:
                t = "Costs: {}".format(i.cost)
                if i.damage != 0:
                    t += ", damage + {}".format(i.damage)
                if i.weaponskill != 0:
                    t += ", weaponskill + {}".format(i.weaponskill)
                if i.critical != 0:
                    t += ", critical + {}".format(i.critical)
                embed.add_field(name=i.name, value=t, inline=False)
            await self.bot.say(embed=embed)
            return
        try:
            weapon = self.weapons[int(args[0])-1]
        except ValueError:
            await self.bot.say("That is not a weapon sold in this part of the country")
            return
        if not player.buyWeapon(weapon):
            await self.bot.say("You do not have the money to buy the {}".format(weapon.name))
            return
        await self.bot.say("You have acquired the {} for {}{}".format(weapon.name, moneysign, weapon.cost))

    # {prefix}train
    @commands.command(pass_context=1, help="Train your skills!")
    async def train(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            embed = discord.Embed(colour=SHOP_EMBED_COLOR)
            embed.set_author(name="Available Training", icon_url=ctx.message.author.avatar_url)
            for i in rpgc.trainingitems.values():
                embed.add_field(name=i.name, value="Minutes per statpoint: {}".format(i.cost))
            await self.bot.say(embed=embed)
            return
        training = args[0]
        if training in ['ws', 'weapon']:
            training = "weaponskill"
        elif training in ['hp', 'h', 'health']:
            training = "maxhealth"
        training = rpgc.trainingitems.get(training)
        if training==None:
            await self.bot.say("Thats not an available training")
            return
        try:
            a = int(args[1])
        except ValueError:
            a = math.ceil(rpgchar.mintrainingtime/training.cost)
        except IndexError:
            a = math.ceil(rpgchar.mintrainingtime/training.cost)

        player = self.bot.rpggame.getPlayerData(ctx.message.author.id, ctx.message.author.display_name)
        if player.busydescription != rpgchar.NONE:
            await self.bot.say("Please make sure you finish your other shit first")
            return
        c = ctx.message.channel
        if c.is_private:
            c = ctx.message.author
        if not player.setBusy(rpgchar.TRAINING, math.ceil(a*training.cost), c.id):
            await self.bot.say("You can train between {} and {} points".format(math.ceil(rpgchar.mintrainingtime/training.cost), math.floor(rpgchar.maxtrainingtime/training.cost)))
            return
        player.buyItem(training, amount=a)
        await self.bot.say("{}, you are now training your {} for {} minutes".format(ctx.message.author.mention, training.name, int(math.ceil(a*training.cost))))
