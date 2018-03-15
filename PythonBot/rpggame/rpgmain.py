import asyncio, datetime, constants, discord, log, math, pickle, random, requests, removeMessage, ipdb, os, os.path, logging
from rpggame import rpgcharacter as rpgchar, rpgdbconnect as dbcon, rpgshop, rpgconstants as rpgc, rpgweapon as rpgw, rpgarmor as rpga
from discord.ext import commands
from discord.ext.commands import Bot
from PIL import Image, ImageFont, ImageDraw 
from io import BytesIO

RPGSTATSFILE = 'logs/rpgstats.txt'
RPG_EMBED_COLOR = 0x710075
STANDARDBATTLETURNS = 30
BATTLETURNS = {"Bossbattle" : 99}

class RPGGame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bossparties = {}
        self.players = {}
        self.gameInit()

    def addHealthRep(self, embed : discord.Embed, players : [rpgchar.RPGCharacter]):
        hrep = ""
        for m in players:
            hrep += m.name + " ({})\n".format(m.health)
        if len(hrep) > 0:
            embed.add_field(name="Healthreport", value=hrep, inline=False)

    async def resolveBattle(self, battlename : str, channel : discord.Channel, p1 : [rpgchar.RPGCharacter], p2 : [rpgchar.RPGMonster()], short=False, thumbnail=None):
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        if thumbnail != None:
            embed.set_thumbnail(url=thumbnail)
        title = ""
        if len(p1)==1:
            title += "{} ({}hp, {})".format(p1[0].name, p1[0].health, rpgc.elementnames.get(p1[0].getElement())[0])
        else:
            title += "A party of {}".format(len(p1))
        title += " vs "
        if len(p2)==1:
            title += "{} ({}hp, {})".format(p2[0].name, p2[0].health, rpgc.elementnames.get(p2[0].getElement())[0])
        else:
            title += "A party of {}".format(len(p2))
        embed.add_field(name=battlename, value=title, inline=False)
        battlereport = ""
        i = 0
        h1 = []
        h2 = []
        for i in range(len(p1)):
            h1.append(p1[i].health)
        for i in range(len(p2)):
            h2.append(p2[i].health)
        turns = BATTLETURNS.get(battlename)
        if turns==None:
            turns=STANDARDBATTLETURNS
        while (i<turns) & (sum([x.health for x in p1]) > 0) & (sum([x.health for x in p2]) > 0):
            for attacker in p1:
                if attacker.health > 0:
                    defs = [x for x in p2 if x.health > 0]
                    if len(defs)<=0:
                        break
                    defender = defs[random.randint(0,len(defs)-1)]
                    ws = random.randint(0, max(attacker.getWeaponskill(), attacker.getCritical()) + defender.getWeaponskill())
                    if (ws < max(attacker.getWeaponskill(), attacker.getCritical())):
                        if ws < attacker.getCritical():
                            damage = int(math.floor((2.5+(0.05*max(0, attacker.getCritical() - attacker.getWeaponskill())))*attacker.getDamage(defender.getElement())))
                            battlereport += "\nCritical hit! **{}** hit **{}** for **{}**".format(attacker.name, defender.name, damage)
                        else:
                            damage = int(math.floor(math.sqrt(random.randint(100, 400)/100) * attacker.getDamage(defender.getElement())))
                            battlereport += "\n**{}** attacked **{}** for **{}**".format(attacker.name, defender.name, damage)
                        if battlename=="Mockbattle":
                            defender.addHealth(-1*damage, death=False)
                        else:
                            defender.addHealth(-1*damage)
            p3 = p1
            p1 = p2
            p2 = p3
            i += 1
        if len(battlereport)>1000:
            print(battlereport)
            short=True
        if not short:
            if len(battlereport)>0:
                embed.add_field(name="Battlereport", value=battlereport, inline=False)
        if (sum([x.health for x in p1]) <= 0):
            if (len(p1)==1) & (len(p2)==1):
                embed.add_field(name="Result", value="{} ({}) laughs while walking away from {}'s corpse".format(p2[0].name, p2[0].health, p1[0].name), inline=False)
            else:
                embed.add_field(name="Result", value="{}'s party completely slaughtered {}'s party".format(p2[0].name, p1[0].name), inline=False)
                self.addHealthRep(embed, (p1+p2))
        else:
            embed.add_field(name="Result", value="The battle lasted long, both parties are exhausted.\nThey agree on a draw this time", inline=False)
            self.addHealthRep(embed, (p1+p2))
        if i%2==1:
            p3 = p1
            p1 = p2
            p2 = p3
        if battlename == "Mockbattle":
            for i in range(len(p1)):
                p1[i].health = h1[i]
            for i in range(len(p2)):
                p2[i].health = h2[i]
        try:
            await self.bot.send_message(channel, embed=embed)
        except discord.errors.HTTPException:
            try:
                await self.bot.send_message(channel, title)
                await self.bot.send_message(channel, battlereport)
            except discord.errors.HTTPException:
                await self.bot.send_message(channel, "Rip bossbattle")
                print(title)
                print(battlereport)
        if sum([(x.health/x.getMaxhealth()) for x in p1]) > sum([(x.health/x.getMaxhealth()) for x in p2]):
            return 1
        return 2 

    async def bossbattle(self):
        print("Boss time!")
        for serverid in self.bossparties:
            party = self.bossparties.get(serverid)
            if len(party) > 0:
                channel = self.bot.get_channel(dbcon.getRPGChannel(str(serverid)))
                if channel == None:
                    print("No channel for {}".format(serverid))
                    return
                lvl = max([x.getBosstier() for x in party])
                bosses = []
                while (3*len(bosses)) < len(party):
                    (name, elem, pic) = random.choice(rpgc.bosses)
                    bosses.append(rpgchar.RPGMonster(name=name, health=int(47*lvl*lvl), damage=int(lvl*lvl), ws=int(lvl*lvl*0.5), element=elem))
                winner = await self.resolveBattle("Bossbattle", channel, party, bosses, thumbnail=pic)
                if winner==1:
                    for p in party:
                        p.addExp(32*lvl*lvl*len(bosses)/len(party))
                        p.addBosstier()
        for p in self.players.values():
            if p.busydescription == rpgchar.BOSSRAID:
                p.resetBusy()
        self.bossparties = {}

    async def adventureEncounter(self, player : rpgchar.RPGPlayer, channel : discord.Channel):
        (name, elem, pic) = random.choice(rpgc.monsters)
        lvl = player.getLevel()
        winner = await self.resolveBattle("Adventure encounter", channel, [player], [rpgchar.RPGMonster(name=name, health=(int(10+math.floor(player.exp/95))), damage=int(math.floor(7*lvl)), ws=int(math.floor(1+(0.07*(player.exp)**(0.6)))), element=elem)], short=False, thumbnail=pic)
        if winner==1:
            player.addExp(100*player.getLevel())

    async def adventureSecret(self, player : rpgchar.RPGPlayer, channel : discord.Channel):
        list = rpgc.adventureSecrets
        (name, stat, amount) = list[random.randint(0, len(list)-1)]
        if stat.lower()=="health":
            player.addHealth(amount)
        elif stat.lower()=="weaponskill":
            player.weaponskill += amount
        elif stat.lower()=="money":
            player.money += amount
        elif stat.lower()=="exp":
            player.exp += amount
        elif stat.lower()=="damage":
            player.damage += amount
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Adventure secret found", value="{}, {}\n{} +{}".format(player.name, name, stat, amount))
        await self.bot.send_message(channel, embed=embed)

    def getBossparties(self):
        parties = {}
        for p in self.players.values():
            if p.busydescription == rpgchar.BOSSRAID:
                party = parties.get(p.busychannel)
                if party is None:
                    party = []
                    self.bossparties[p.busychannel] = party
                party.append(p)
        return parties

    def gameInit(self):
        self.players = dbcon.getBusyPlayers()
        self.bossparties = self.getBossparties()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        print("RPG Gameloop started!")

    async def gameTick(self, time):
        try:
            if time.minute%5 == 0:
                print(time)
            # Saving stats to db
            if time.minute%15 == 0:
                p = self.players.values()
                if len(p) > 0:
                    dbcon.updatePlayers(p)
                    l = list(self.players.keys())
                    for i in l:
                        player = self.players.get(i)
                        if (player.busydescription == rpgchar.NONE) & (player.health >= player.getMaxhealth()):
                            self.players.pop(i)
                print("Players saved")
            # Bossraids
            if time.minute == 55:
                for p in self.bossparties:
                    await self.bot.send_message(self.bot.get_channel(dbcon.getRPGChannel(str(p))), "A party of {} is going to fight the boss in 5 minutes!!\nJoin fast if you want to participate".format(len(self.bossparties.get(p))))
            if time.minute == 0:
                await self.bossbattle()
                self.bot.rpgshop.weapons = {}
                self.bot.rpgshop.armors = {}
            # Player is busy
            for u in list(self.players.values()):
                if u.health < u.getMaxhealth():
                    u.autoHealthRegen()
                if u.busydescription != rpgchar.NONE:
                    if not(u.busydescription in [rpgchar.BOSSRAID]):
                        u.busytime -= 1
                    c = self.bot.get_channel(str(u.busychannel))
                    if c is None:
                        c = await self.bot.get_user_info(str(u.busychannel))
                    if u.busydescription == rpgchar.ADVENTURE:
                        if c != None:
                            if(random.randint(0,4)<=0):
                                await self.adventureEncounter(u, c)
                    if (u.busydescription in [rpgchar.ADVENTURE, rpgchar.WANDERING]) and (random.randint(0,14)<=0):
                        await self.adventureSecret(u, c)
                    if (u.busytime <= 0):
                        embed = discord.Embed(colour=RPG_EMBED_COLOR)
                        if u.busydescription == rpgchar.ADVENTURE:
                            type = "adventure"
                            action = "adventuring"
                        elif u.busydescription == rpgchar.TRAINING:
                            type = action = "training"
                        elif u.busydescription == rpgchar.WANDERING:
                            type = action = "wandering"
                        else:
                            type = action = "Unknown"
                        if u.health > 0:
                            embed.add_field(name="Ended {}".format(type), value="You are now done {}".format(action))
                        else:
                            embed.add_field(name="You Died".format(type), value="You were killed on one of your adventures".format(action))
                            embed.set_thumbnail(url="https://res.cloudinary.com/teepublic/image/private/s--_1_FlGAa--/t_Preview/b_rgb:191919,c_limit,f_jpg,h_630,q_90,w_630/v1466191557/production/designs/549487_1.jpg")
                        c = await self.bot.get_user_info(str(u.userid))
                        if c != None:
                            await self.bot.send_message(c, embed=embed)
                        else:
                            print("Channel not found, {} is done with {}".format(u.name, u.busydesription))
                        u.resetBusy()
        except Exception as e:
            print(e)
            self.logger.exception(e)

    def getParty(self, serverid):
        party = self.bossparties.get(serverid)
        if party == None:
            party = []
            self.bossparties[serverid] = party
        return party

    def getPlayerData(self, userid, name=None):
        p = self.players.get(str(userid))
        if p == None:
            p = dbcon.getPlayer(str(userid))
            self.players[str(userid)] = p
        if name != None:
            p.name = name
        return p

    async def handle(self, message : discord.Message):
        data = self.getPlayerData(message.author.id, name=message.author.display_name)
        if data.role not in rpgc.names.get("role"): 
            return
        if data.busydescription in [rpgchar.ADVENTURE, rpgchar.WANDERING]:
            return
        i = round(pow((data.getLevel())+1, 1/3)  # levelbonus
                *max(0, min(50, (len(message.content) - 3) / 2))); # Textbonus
        if data.busydescription in [rpgchar.TRAINING, rpgchar.BOSSRAID]:
            i *= 0.5
        data.addMoney(int(i))
        data.addExp(1)

    def quit(self):
        #save rpgstats
        dbcon.updatePlayers(self.players.values())
        print("RPGStats saved")

    # RPG intro/help
    @commands.group(pass_context=1, aliases=["b&d", "bnd"], help="Get send an overview of the rpg game's commands".format(constants.prefix))
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Your '{}rpg' has been heard, you will be send the commands list for the rpg game".format(constants.prefix))
            embed = discord.Embed(colour=RPG_EMBED_COLOR)
            embed.set_author(name="RPG Help", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Introduction", value="Welcome adventurer, this game grants you the opportunity to slay monsters and rule a realm. You can train yourself and buy upgrades at the shop, and when you are done with adventuring, you can even challenge a boss every hour with a group of friends.", inline=False)
            embed.add_field(name="Basics", value="Talking gains you extra money\nIf it sounds like a logical alias, it probably is\nYour health regenerates every minute\nThe weaponsmith refills his inventory every hour\nA boss can be fought at the hour mark", inline=False)
            embed.add_field(name="{}rpg [role|r|class|c]".format(constants.prefix), value="Switch your role on the battlefield (A role is needed to play the game)", inline=False)
            embed.add_field(name="{}rpg [adventure|a] <minutes>".format(constants.prefix), value="Go on an adventure, find monsters to slay to gain exp", inline=False)
            embed.add_field(name="{}rpg [wander|w] <minutes>".format(constants.prefix), value="Go wandering, you might find a great treasure!", inline=False)
            embed.add_field(name="{}rpg [battle|b] <user>".format(constants.prefix), value="Battle another user for the lolz, no exp will be gained and no health will be lost", inline=False)
            embed.add_field(name="{}rpg [info|i|stats|status] <user>".format(constants.prefix), value="Show your or another user's game statistics", inline=False)
            embed.add_field(name="{}rpg [info|i|stats|status] [weapon|w|armor|a] <user>".format(constants.prefix), value="Show your or another user's weapon statistics", inline=False)
            embed.add_field(name="{}rpg [join|j]".format(constants.prefix), value="Join the hourly boss raid (warning, don't try this alone)", inline=False)
            embed.add_field(name="{}rpg [party|p]".format(constants.prefix), value="Show the brave souls that will be attacking the boss at the hour mark", inline=False)
            await self.bot.send_message(ctx.message.author, embed=embed)
            
            embed = discord.Embed(colour=RPG_EMBED_COLOR)
            embed.add_field(name="{}rpg [top|t] <exp|money|bosstier> <page>".format(constants.prefix), value="Show the best players of the game", inline=False)
            embed.add_field(name="{}rpg [levelup|lvl|lvlup]".format(constants.prefix), value="Choose a reward when you leveled up", inline=False)
            embed.set_author(name="RPG Help", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="{}rpg king".format(constants.prefix), value="Show the current King of the server", inline=False)
            embed.add_field(name="{}rpg king [c|b|challenge|battle]".format(constants.prefix), value="Challenge the current King and try to take his spot (level 10+)", inline=False)
            embed.add_field(name="{}shop".format(constants.prefix), value="Show the rpg shop inventory", inline=False)
            embed.add_field(name="{}shop [item|i|buy] <item> <amount>".format(constants.prefix), value="Buy <amount> of <item> from the shop", inline=False)
            embed.add_field(name="{}shop [weapon|w] <number>".format(constants.prefix), value="Buy a certain weapon from the shop (hourly refresh of stock)", inline=False)
            embed.add_field(name="{}shop [armor|a] <number>".format(constants.prefix), value="Buy a certain armor from the shop (hourly refresh of stock)", inline=False)
            embed.add_field(name="{}train".format(constants.prefix), value="Show the available training sessions", inline=False)
            embed.add_field(name="{}train <stat> <amount>".format(constants.prefix), value="Train yourself for <amount> points of the chosen <stat>", inline=False)
            embed.set_footer(text="Suggestions? Feel free to message me or join my server (see {}help for details)".format(constants.prefix))
            await self.bot.send_message(ctx.message.author, embed=embed)
    
    # {prefix}rpg adventure #
    @rpg.command(pass_context=1, aliases=["a"], help="Go on an adventure!")
    async def adventure(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        if len(args) > 0:
            try:
                n = int(args[0])
            except ValueError:
                n = 10
        else:
            n = 10
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("You are already doing other things")
            return
        if n<rpgchar.minadvtime:
            await self.bot.say("You came back before you even went out, 0 exp earned")
            return
        if n>rpgchar.maxadvtime:
            await self.bot.say("You do not have the stamina to go on that long of an adventure")
            return
        c = ctx.message.channel
        if c.is_private:
            c = ctx.message.author
        if not data.setBusy(rpgchar.ADVENTURE, n, c.id):
            await self.bot.say("{}, something went terribly wrong while trying to get busy...".format(ctx.message.author.mention))
            return
        await self.bot.say("{}, you are now adventuring for {} minutes, good luck!".format(ctx.message.author.mention, n))

    # {prefix}rpg battle <user>
    @rpg.command(pass_context=1, aliases=["b"], help="Battle a fellow discord ally to a deadly fight!")
    async def battle(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        if len(ctx.message.mentions)<1:
            await self.bot.say("You need to tag someone to battle with!")
            return
        if ctx.message.mentions[0] == ctx.message.author:
            await self.bot.say("Suicide is never the answer :angry:")
            return
        attacker = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        #if attacker.busydescription != rpgchar.NONE:
        #    await self.bot.say("You are already doing something else at the moment...")
        #    return
        defender = self.getPlayerData(ctx.message.mentions[0].id, name=ctx.message.mentions[0].display_name)
        #if defender.busydescription != rpgchar.NONE:
        #    await self.bot.say("Your opponent is unfindable at the moment.\nYou should catch him off guard when he is resting.")
        #    return
        await self.resolveBattle("Mockbattle", ctx.message.channel, [attacker], [defender], thumbnail=ctx.message.author.avatar_url)

    # {prefix}rpg info [weapon|w|armor|a] <user>
    @rpg.command(pass_context=1, aliases=['i', 'stats', 'status'], help="Show the character's status information!")
    async def info(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)>0:
            data = self.getPlayerData(ctx.message.mentions[0].id, name=ctx.message.mentions[0].display_name)
        else:
            data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, that player is still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        if len(args)>0:
            if args[0] in ['w', 'weapon']:
                embed = discord.Embed(colour=RPG_EMBED_COLOR)
                embed.set_author(name="{}'s weapon".format(data.name), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Weapon's name", value=data.weapon.name, inline=False)
                embed.add_field(name="Original cost", value=data.weapon.cost, inline=False)
                embed.add_field(name="Element", value=rpgc.elementnames.get(data.weapon.element)[0], inline=False)
                if data.weapon.damage != 0:
                    embed.add_field(name="Damage", value=data.weapon.damage, inline=False)
                if data.weapon.weaponskill != 0:
                    embed.add_field(name="Weaponskill", value=data.weapon.weaponskill, inline=False)
                if data.weapon.critical != 0:
                    embed.add_field(name="Critical", value=data.weapon.critical, inline=False)               
                await self.bot.send_message(ctx.message.channel, embed=embed)
                return
            if args[0] in ['a', 'armor']:
                embed = discord.Embed(colour=RPG_EMBED_COLOR)
                embed.set_author(name="{}'s armor".format(data.name), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Armor's name", value=data.armor.name, inline=False)
                embed.add_field(name="Original cost", value=data.armor.cost, inline=False)
                embed.add_field(name="Element", value=rpgc.elementnames.get(data.armor.element)[0], inline=False)
                if data.armor.maxhealth != 0:
                    embed.add_field(name="Maxhealth", value=data.armor.maxhealth, inline=False)
                if data.armor.healthregen != 0:
                    embed.add_field(name="Healthregeneration", value=data.armor.healthregen, inline=False)
                if data.armor.money != 0:
                    embed.add_field(name="Extra money", value="{}%".format(data.armor.money), inline=False)
                await self.bot.send_message(ctx.message.channel, embed=embed)
                return
        try:
            im = Image.open("/home/nya/PythonBot/PythonBot/rpggame/{}.png".format(data.role.lower()))
        except:
            im = Image.open("/home/nya/PythonBot/PythonBot/rpggame/undead.png")
        if ctx.message.channel.is_private:
            url = ctx.message.author.avatar_url
        else:
            url = ctx.message.server.get_member(str(data.userid)).avatar_url
        pp = Image.open(BytesIO(requests.get(url).content))
        pp = pp.resize((60,60))
        im.paste(pp, (235,5))

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("/home/nya/ringbearer/RINGM___.TTF", 12)
        color = (255,255,255)
        nameoffset = 18
        statoffset = nameoffset + 98
        topoffset = 18
        next = 23

        if len(data.name) < 12:
            data.name+= " 's informations"
        draw.text((nameoffset, topoffset),data.name + ":",color,font=font)
        draw.text((nameoffset, topoffset+next),str(data.role),color,font=font)         
        if data.levelups > 0:
            stats = "Level up available!"
        else:
            if data.exp > 1000000000:
                shortexp = str(int(data.exp / 1000000000)) + "b"
            elif data.exp > 1000000:
                shortexp = str(int(data.exp / 1000000)) + "m"
            elif data.exp > 1000:
                shortexp = str(int(data.exp / 1000)) + "k"
            else:
                shortexp = str(int(data.exp))
            stats = "lvl {} ({} xp)".format(data.getLevel(), shortexp)        
        draw.text((statoffset, topoffset+next),stats,color,font=font) 
        draw.text((nameoffset, topoffset+2*next),"Boss Tier:",color,font=font)
        draw.text((statoffset, topoffset+2*next),"{}".format(data.getBosstier()),color,font=font)         
        if data.health <= 0:
            stats = "Dead"
        elif data.busydescription == rpgchar.ADVENTURE:
            stats = "Adventuring for {}m".format(data.busytime)
        elif data.busydescription == rpgchar.TRAINING:
            stats = "Training for {}m".format(data.busytime)
        elif data.busydescription == rpgchar.BOSSRAID:
            stats = "Waiting for the bossbattle"
        elif data.busydescription == rpgchar.WANDERING:
            stats = "Wandering for {}m".format(data.busytime)
        else:
            stats = "Alive"
        draw.text((nameoffset, topoffset+3*next),"Status:",color,font=font)
        draw.text((statoffset, topoffset+3*next),stats,color,font=font)   
        draw.text((nameoffset, topoffset+4*next),"Money:",color,font=font)
        draw.text((statoffset, topoffset+4*next),"{}{}".format(rpgshop.moneysign, data.money),color,font=font)
        draw.text((nameoffset, topoffset+5*next),"Health:",color,font=font)
        draw.text((statoffset, topoffset+5*next),"{}/{}".format(data.health,data.getMaxhealth()),color,font=font)
        draw.text((nameoffset, topoffset+6*next),"Damage:",color,font=font)
        draw.text((statoffset, topoffset+6*next),"{}".format(data.getDamage()),color,font=font)
        draw.text((nameoffset, topoffset+7*next),"Weaponskill:",color,font=font)
        draw.text((statoffset, topoffset+7*next),"{}".format(data.getWeaponskill()),color,font=font)
        draw.text((nameoffset, topoffset+8*next),"Critical:",color,font=font)
        draw.text((statoffset, topoffset+8*next),"{}".format(data.getCritical()),color,font=font)

        imname = '/home/nya/PythonBot/PythonBot/temp/{}.png'.format(ctx.message.author.id)
        im.save(imname)
        await self.bot.send_file(ctx.message.channel, imname)
        os.remove(imname)

    # {prefix}rpg join
    @rpg.command(pass_context=1, aliases=["j"], help="Join a raid to kill a boss!")
    async def join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("{}, finish your current task first, then you can join the boss raid party!".format(ctx.message.author.mention))
            return
        if ctx.message.channel.is_private:
            await self.bot.say("This command cannot work in a private channel")
            return
        party = self.getParty(ctx.message.server.id)
        if data in party:
            await self.bot.say("{}, you are already in the boss raid party...".format(ctx.message.author.mention))
            return
        party.append(data)
        data.setBusy(rpgchar.BOSSRAID, 1, ctx.message.server.id)
        await self.bot.say("{}, prepare yourself! You and your party of {} will be fighting the boss at the hour mark!".format(ctx.message.author.mention, len(party)))

    # {prefix}rpg king
    @rpg.command(pass_context=1, aliases=["k"], help="The great king's game!")
    async def king(self, ctx, *args):
        kingname = "OMEGA dank L0rD on the ServEr to get all the loli traps"
        await removeMessage.deleteMessage(self.bot, ctx)
        if ctx.message.channel.is_private:
            await self.bot.say("This command cannot work in a private channel")
            return
        king = dbcon.getKing(ctx.message.server.id)
        if (len(args) <= 0):
            if king is None:
                await self.bot.say("There is currently no {} in {}".format(kingname, ctx.message.server.name))
                return
            await self.bot.say("The current {} of {} is {}".format(kingname, ctx.message.server.name, ctx.message.server.get_member(str(king)).display_name))
            return
        data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("Please finish what you are doing before a fight")
            return
        now = datetime.datetime.now()
        if data.kingtimer != 0:
            if (now - datetime.datetime.fromtimestamp(data.kingtimer)).seconds < 3600:
                await self.bot.say("You are still tired from your last battle, rest for an hour or so and you can try again")
                return
        if dbcon.isKing(data.userid):
            await self.bot.say("You are already a {} of another world".format(kingname))
            return
        if not(args[0] in ["c", "b", "challenge", "battle"]):
            return
        if data.getLevel() < 10:
            await self.bot.say("You need to be at least level 10 to challenge the current {}".format(kingname))
            return
        if king is None:
            dbcon.setKing(data.userid, ctx.message.server.id)
            await self.bot.say("You are now the {0} of {1}!\nLong live the {0}!".format(kingname, ctx.message.server.name))
            return
        if king == data.userid:
            await self.bot.say("But you are already the {} of {}...".format(kingname, ctx.message.server.name))
            return
        kingdata = self.getPlayerData(king)
        if (await self.resolveBattle("Kingsbattle", ctx.message.channel, [data], [kingdata])) == 1:
            winner = data
            dbcon.setKing(data.userid, ctx.message.server.id)
            await self.bot.say("{0} beat down {1}\n{0} is now the {2} of {3}!".format(data.name, kingdata.name, kingname, ctx.message.server.name))
        else:
            winner = kingdata
            await self.bot.say("{0} beat down {1}\n{0} remains the true {2} of {3}!".format(kingdata.name, data.name, kingname, ctx.message.server.name))
        data.kingtimer = now.timestamp()
        kingdata.kingtimer = now.timestamp()
        winner.health = winner.getMaxhealth()
        winner.levelups += 1

    async def addLevelup(self, data, channel, reward):
        if reward==1:
            data.setMaxhealth(data.maxhealth + 80)
            await self.bot.send_message(channel, "Your base maximum health is now {}".format(data.maxhealth))
        elif reward==2:
            data.weaponskill += 2
            await self.bot.send_message(channel, "Your base weaponskill is now {}".format(data.weaponskill))
        elif reward==3:
            data.damage += 30
            await self.bot.send_message(channel, "Your base damage is now {}".format(data.damage))
        else:
            await self.bot.send_message(channel, "Dunno what you mean tbh")
            return False
        return True

    # {prefix}rpg levelup
    @rpg.command(pass_context=1, aliases=["lvlup", "lvl"], help="Join a raid to kill a boss!")
    async def levelup(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.levelups <= 0:
            await self.bot.say("You have no level-ups available")
            return
        
        if len(args) <= 0:
            while data.levelups > 0:
                await self.bot.say("Available rewards are:\n1)\t+80 hp\n2)\t+2 ws\n3)\t+30 damage")
                m = await self.bot.wait_for_message(timeout=60, author=ctx.message.author, channel=ctx.message.channel)
                if m==None:
                    return
                try:
                    num = int(m.content)
                    if await self.addLevelup(data, ctx.message.channel, num):
                        data.levelups -= 1
                except ValueError:
                    return
        else:
            try:
                if await self.addLevelup(data, ctx.message.channel, int(args[0])):
                    data.levelups -= 1
            except ValueError:
                await self.bot.say("Thats not even a number...")
                return

    # {prefix}rpg party
    @rpg.command(pass_context=1, aliases=["p"], help="All players gathered to kill the boss")
    async def party(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ctx.message.channel.is_private:
            await self.bot.say("This command cannot work in a private channel")
            return
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        party = self.getParty(ctx.message.server.id)
        if len(party) <= 0:
            await self.bot.say("There is no planned boss raid, but you are welcome to start a party!")
            return
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Boss raiding party", value="{} adventurers".format(len(party)), inline=False)
        embed.add_field(name="Estimated boss level", value=max([x.getBosstier() for x in party]), inline=False)
        m = ""
        for n in party:
            member = ctx.message.server.get_member(str(n.userid))
            m += "{}, level {}\n".format(member.display_name, n.getLevel())
        embed.add_field(name="Adventurers", value=m, inline=False)
        await self.bot.say(embed=embed)

    # {prefix}rpg role
    @rpg.command(pass_context=1, aliases=["r", "class", "c"], help="Switch your role on the battlefield")
    async def role(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if len(args) <= 0:
            await self.bot.say("{}, the currently available roles are: {}".format(ctx.message.author.mention, ", ".join(rpgc.names.get("role"))))
            return
        role = " ".join(args)
        if role == data.role:
            await self.bot.say("{}, that is already your current role...".format(ctx.message.author.mention))
            return
        if role in rpgc.names.get("role"):
            data.role = role
            await self.bot.say("{}, you now have the role of {}".format(ctx.message.author.mention, role))
            return
        await self.bot.say("{}, that is not a role available to a mere mortal".format(ctx.message.author.mention))

    def getGroup(self, s : str):
        if s in ['m', 'money']:
            return "money"
        if s in ['b', 'bt', 'bosstier']:
            return "bosstier"
        return "exp"

    # {prefix}rpg top <exp|money|bosstier> <amount>
    @rpg.command(pass_context=1, aliases=['t'], help="Show the people with the most experience!")
    async def top(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ctx.message.channel.is_private:
            await self.bot.say("This command does not work in a private channel")
            return
        if len(args) > 0:
            if len(args) > 1:
                try:
                    n = int(args[1])-1
                except ValueError:
                    n = 0
                group = self.getGroup(args[0])
            else:
                try:
                    n = int(args[0])-1
                    group = "exp"
                except ValueError:
                    n = 0
                    group = self.getGroup(args[0])
        else:
            n = 0
            group = "exp"

        # Construct return message
        USERS_PER_PAGE = 10
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="RPG top players", value="Page " + str(n+1), inline=False)
        dbcon.updatePlayers(self.players.values())
        list = dbcon.getTopPlayers(group, (n+1)*USERS_PER_PAGE)
        if (len(list) < (USERS_PER_PAGE*n)):
            await self.bot.say("There are only {} pages...".format(math.ceil(len(list)/USERS_PER_PAGE)))
            return
        end = (USERS_PER_PAGE*(n+1))
        if end > len(list):
            end = len(list)
        i = (USERS_PER_PAGE*n)
        result = ""
        
        for m in list[i:end]:
            i += 1
            try:
                name = ctx.message.server.get_member(str(m[0])).display_name
            except AttributeError:
                name = "id{}".format(m[0])
            if group=="money":
                result += "Rank {}:\n\t**{}**, {}{}\n".format(i, name, rpgshop.moneysign, m[1])
            elif group=="bosstier":
                result += "Rank {}:\n\t**{}**, tier {}\n".format(i, name, m[1])
            else:
                result += "Rank {}:\n\t**{}**, {}xp (L{})\n".format(i, name, m[1], rpgchar.getLevelByExp(m[1]))
        embed.add_field(name="Ranks and names", value=result)
        await self.bot.send_message(ctx.message.channel, embed=embed)
    
    # {prefix}rpg wander #
    @rpg.command(pass_context=1, aliases=["w"], help="Wander in the beautiful country")
    async def wander(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.role == "Undead":
            await self.bot.say("{}, You are still Undead. Please select a class with '>rpg role' in order to start to play!".format(ctx.message.author.mention))
            return
        if len(args) > 0:
            try:
                n = int(args[0])
            except ValueError:
                n = 10
        else:
            n = 10
        data = data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("You are already doing other things")
            return
        if not(rpgchar.minwandertime <= n <= rpgchar.maxwandertime):
            await self.bot.say("You can wander between {} and {} minutes".format(rpgchar.minwandertime, rpgchar.maxwandertime))
            return
        c = ctx.message.channel
        if c.is_private:
            c = ctx.message.author
        if not data.setBusy(rpgchar.WANDERING, n, c.id):
            await self.bot.say("{}, something went terribly wrong while trying to get busy...".format(ctx.message.author.mention))
            return
        await self.bot.say("{}, you are now wandering for {} minutes, good luck!".format(ctx.message.author.mention, n))

    # DB commands            
    @rpg.command(pass_context=1, hidden=True, help="Reset channels!")
    async def updatedb(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid or ctx.message.author.id==constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.updatePlayers(self.players.values())
        self.players = {}

    @rpg.command(pass_context=1, hidden=True, help="Reset channels!")
    async def resetchannels(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.initChannels()
        await self.bot.say("RPG channels reset")

    @rpg.command(pass_context=1, hidden=True, help="Reset rpg data!")
    async def resetstats(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid or ctx.message.author.id==constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        self.bossparties = {}
        self.players = {}
        dbcon.resetPlayers()
        await self.bot.say("RPG stats reset")

    @rpg.command(pass_context=1, help="Set rpg channel!")
    async def setchannel(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.setRPGChannel(ctx.message.server.id, ctx.message.channel.id)
        await self.bot.say("This channel is now the rpg channel for this server")

    #money for devs (testing purpose ONLY)
    @rpg.command(pass_context=1, hidden=True, help="Dev money")
    async def cashme(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid or ctx.message.author.id==constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        data = self.getPlayerData(ctx.message.author.id, name=ctx.message.author.display_name)
        data.money += 99999999    

    @rpg.command(pass_context=1, hidden=True, help="Dev trigger bossfights")
    async def triggerbossfights(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid or ctx.message.author.id==constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        await self.bot.rpggame.bossbattle()