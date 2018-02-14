import asyncio, datetime, constants, discord, log, math, pickle, random, removeMessage, sqlite3
import rpggame.rpgcharacter as rpgchar, rpggame.rpgdbconnect as dbcon, rpggame.rpgshop as rpgshop
from discord.ext import commands
from discord.ext.commands import Bot

RPGSTATSFILE = 'logs/rpgstats.txt'
RPG_EMBED_COLOR = 0x710075
BATTLETURNS = 30

class RPGGame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bossparties = {}
        self.players = {}
        self.bot.loop.create_task(self.gameloop())

    async def resolveBattle(self, channel : discord.Channel, p1 : [rpgchar.RPGCharacter], p2 : [rpgchar.RPGMonster()], short=False, mockbattle=False):
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        title = ""
        if len(p1)==1:
            title += "{} ({})".format(p1[0].name, p1[0].health)
        else:
            title += "A party of {}".format(len(p1))
        title += " vs "
        if len(p2)==1:
            title += "{} ({})".format(p2[0].name, p2[0].health)
        else:
            title += "A party of {}".format(len(p2))
        embed.add_field(name="Battle", value=title, inline=False)
        battlereport = ""
        i = 0
        h1 = []
        h2 = []
        for i in range(len(p1)):
            h1.append(p1[i].health)
        for i in range(len(p2)):
            h2.append(p2[i].health)
        while (i<BATTLETURNS) & (sum([x.health for x in p1]) > 0) & (sum([x.health for x in p2]) > 0):
            for attacker in p1:
                defender = p2[random.randint(0,len(p2)-1)]
                ws = random.randint(0, attacker.weaponskill + defender.weaponskill)
                if (ws < attacker.weaponskill):
                    damage = math.floor((random.randint(100, 200) * attacker.damage)/100);
                    defender.addHealth(-1*damage)
                    battlereport += "\n**{}** attacked **{}** for **{}**".format(attacker.name, defender.name, damage)
            p3 = p1
            p1 = p2
            p2 = p3
            #print(p1.name + ": " + str(p1.health) + " | " + p2.name + " : " + str(p2.health))
            i += 1
        
        if not short:
            embed.add_field(name="Battlereport", value=battlereport, inline=False)
        if(len(p1)==1) & (len(p2)==1) & (p1[0].health <= 0):
            embed.add_field(name="Result", value="{} ({}) laughs while walking away from {}'s corpse".format(p2[0].name, p2[0].health, p1[0].name), inline=False)
        else:
            embed.add_field(name="Result", value="The battle lasted long, both players are exhausted.\nThey agree on a draw this time", inline=False)
            hrep = ""
            for m in (p1+p2):
                hrep += m.name + " ({})\n".format(m.health)
            embed.add_field(name="Healthreport", value=hrep, inline=False)
        if mockbattle:
            for i in range(len(p1)):
                p1[i].health = h1[i]
            for i in range(len(p2)):
                p2[i].health = h2[i]
        else:
            for m in (p1+p2):
                if isinstance(m, rpgchar.RPGPlayer):
                    m.addExp(100*m.getLevel())
        await self.bot.send_message(channel, embed=embed);

    async def bossbattle(self):
        print("Boss time!")
        for serverid in self.bossparties:
            party = self.bossparties.get(serverid)
            if len(party) > 0:
                channel = self.getRPGChannel(str(serverid))
                boss = rpgchar.RPGMonster(name="Dark Eldar Lord", health=250)
                await self.resolveBattle(channel, party, [boss])
                return

    async def gameloop(self):
        await self.bot.wait_until_ready()
        print("RPG Gameloop started!")
        running = True;
        while running:
            time = datetime.datetime.utcnow()
            if time.minute%5 == 0:
                print(time)
            # Saving stats to db
            if time.minute%15 == 0:
                p = self.players.values()
                if len(p) > 0:
                    dbcon.updatePlayers(p)
                    l = list(self.players.keys())
                    for i in l:
                        if self.players.get(i).busydescription == rpgchar.NONE:
                            self.players.pop(i)
                print("Players saved")
            # Bossraids
            if time.minute == 55:
                for p in self.bossparties:
                    await self.bot.send_message(self.getRPGChannel(str(p)), "A party of {} is going to fight the boss in 5 minutes!!\nJoin fast if you want to participate".format(len(self.bossparties.get(p))))
            if time.minute == 0:
                await self.bossbattle()
                self.bossparties = {}
            # Adventures
            for u in list(self.players.values()):
                if u.health < u.maxhealth:
                    u.addHealth(10)
                if u.busydescription != rpgchar.NONE:
                    u.busytime -= 1
                    c = self.bot.get_channel(str(u.busychannel))
                    if u.busydescription == rpgchar.ADVENTURE:
                        if c != None:
                            if(random.randint(0,4)<=0): 
                                await self.resolveBattle(c, [u], [rpgchar.RPGMonster()], short=True)
                    if u.busytime <= 0:
                        embed = discord.Embed(colour=RPG_EMBED_COLOR)
                        if u.busydescription == rpgchar.ADVENTURE:
                            type = "adventure"
                            action = "adventuring"
                        if u.busydescription == rpgchar.TRAINING:
                            type = "training"
                            action = "training"
                        embed.add_field(name="Ended {}".format(type), value="{}, you are now done {}".format(u.name, action))
                        await self.bot.send_message(self.bot.get_channel(u.busychannel), embed=embed)
                        u.resetBusy()

            endtime = datetime.datetime.utcnow()
            #print("Sleeping for " + str(60-(endtime).second) + "s")
            await asyncio.sleep(60-endtime.second)

    def getParty(self, serverid):
        party = self.bossparties.get(serverid)
        if party == None:
            party = []
            self.bossparties[serverid] = party
        return party

    def getPlayerData(self, user : discord.User, name=None):
        p = self.players.get(user.id)
        if p == None:
            p = dbcon.getPlayer(user)
            self.players[user.id] = p
        if name != None:
            p.name = name
        return p

    async def handle(self, message : discord.Message):
        data = self.getPlayerData(message.author, name=message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            return
        i = round(pow((data.getLevel())+1, 1/3)  # levelbonus
                *max(0, min(50, (len(message.content) - 3) / 2))); # Textbonus
        data.addExp(i)

    async def quit(self):
        self.running = False
        #save rpgstats
        dbcon.updatePlayers(self.players.values())
        print("RPGStats saved")

    @commands.group(pass_context=1, aliases=["g"], help="'{}help rpg' for full options".format(constants.prefix))
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Use '{}help rpg' for full options".format(constants.prefix))
    
    # {prefix}rpg adventure #
    @rpg.command(pass_context=1, aliases=["a"], help="Go on an adventure!")
    async def adventure(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) > 0:
            try:
                n = int(args[0])
            except ValueError:
                n = 10
        else:
            n = 10
        data = self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("You are already doing other things")
            return
        if n<rpgchar.minadvtime:
            await self.bot.say("You came back before you even went out, 0 exp earned")
            return
        if n>rpgchar.maxadvtime:
            await self.bot.say("You do not have the stamina to go on that long of an adventure")
            return
        if not data.setBusy(rpgchar.ADVENTURE, n, ctx.message.channel.id):
            await self.bot.say("{}, something went terribly wrong while trying to get busy...".format(ctx.message.author.mention))
            return
        data.setAdventure(n, ctx.message.channel.id)
        await self.bot.say("{}, you are now adventuring for {} minutes, good luck!".format(ctx.message.author.mention, n))

    # {prefix}rpg battle <user>
    @rpg.command(pass_context=1, aliases=["b"], help="Battle a fellow discord ally to a deadly fight!")
    async def battle(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)<1:
            await self.bot.say("You need to tag someone to battle with!")
            return
        if ctx.message.mentions[0] == ctx.message.author:
            await self.bot.say("Suicide is never the answer :angry:")
            return
        attacker = self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name)
        if attacker.busydescription != rpgchar.NONE:
            await self.bot.say("You are already doing something else at the moment...")
            return
        defender = self.getPlayerData(ctx.message.mentions[0], name=ctx.message.mentions[0].display_name)
        if defender.busydescription != rpgchar.NONE:
            await self.bot.say("Your opponent is unfindable at the moment.\nYou should catch him off guard when he is resting.")
            return
        await self.resolveBattle(ctx.message.channel, [attacker], [defender], mockbattle=True)

    # {prefix}rpg info <user>
    @rpg.command(pass_context=1, aliases=['i', 'stats', 'status'], help="Show the character's status information!")
    async def info(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)>0:
            data = self.getPlayerData(ctx.message.mentions[0], name=ctx.message.mentions[0].display_name)
        else:
            data = self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name)
        statnames = "Username:"
        stats = data.name
        statnames += "\nStatus:"
        if data.health <= 0:
            stats += "\nDead"
        elif data.busydescription == rpgchar.ADVENTURE:
            stats += "\nAdventuring for {}m".format(data.busytime)
        elif data.busydescription == rpgchar.TRAINING:
            stats += "\nTraining for {}m".format(data.busytime)
        else:
            stats += "\nAlive"
        statnames += "\nExperience:"
        stats += "\n{} ({})".format(data.exp, data.getLevel())
        statnames += "\nMoney:"
        stats += "\n${}".format(data.money)
        statnames += "\nHealth:"
        stats += "\n{}/{}".format(min(data.health, data.maxhealth),data.maxhealth)
        if data.health > data.maxhealth:
            statnames += "\nArmor:"
            stats += "\n{}".format(data.health - data.maxhealth)
        statnames += "\nDamage:"
        stats += "\n{}".format(data.damage)
        statnames += "\nWeaponskill:"
        stats += "\n{}".format(data.weaponskill)

        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Statname", value=statnames)
        embed.add_field(name="Stats", value=stats)
        await self.bot.say(embed=embed)

    # {prefix}rpg join
    @rpg.command(pass_context=1, aliases=["j"], help="Join a raid to kill a boss!")
    async def join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name)
        if data.busydescription != rpgchar.NONE:
            await self.bot.say("Finish your current task first, then you can join the boss raid party!")
            return
        party = self.getParty(ctx.message.server.id)
        if data in party:
            await self.bot.say("You are already in the boss raid party...")
            return
        party.append(data)
        await self.bot.say("Prepare yourself! You and your party of {} will be fighting the boss at the hour mark!".format(len(party)))

    # {prefix}rpg party
    @rpg.command(pass_context=1, aliases=["p"], help="All players gathered to kill the boss")
    async def party(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        party = self.getParty(ctx.message.server.id)
        if len(party) <= 0:
            await self.bot.say("There is no planned boss raid, but you are welcome to start a party!")
            return
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Boss raiding party", value="{} adventurers".format(len(party)), inline=False)
        m = ""
        for n in party:
            member = ctx.message.server.get_member(str(n.userid))
            m += "{}, level {}\n".format(member.display_name, n.getLevel())
        embed.add_field(name="Adventurers", value=m, inline=False)
        await self.bot.say(embed=embed)

    # {prefix}rpg top #
    @rpg.command(pass_context=1, aliases=[], help="Show the people with the most experience!")
    async def top(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) > 0:
            try:
                n = int(args[0])-1
            except ValueError:
                n = 0
        else:
            n = 0
        # Construct return message
        USERS_PER_PAGE = 10
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="RPG top players", value="Page " + str(n+1), inline=False)
        dbcon.updatePlayers(self.players.values())
        list = dbcon.getTopPlayers()
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
            member = self.players.get(str(m[0]))
            if member != None:
                name = member.name
                exp = member.exp
                lvl = member.getLevel()
            else:
                try:
                    name = ctx.message.server.get_member(str(m[0])).display_name
                except AttributeError:
                    name = "id{}".format(m[0])
                exp = m[1]
                lvl = rpgchar.getLevelByExp(m[1])
            result += "Rank {}:\n\t**{}**, {}xp (L{})\n".format(i, name, exp, lvl)
        embed.add_field(name="Ranks and names", value=result)
        await self.bot.send_message(ctx.message.channel, embed=embed)
    
    # DB commands            
    @rpg.command(pass_context=1, help="Reset channels!")
    async def updatedb(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.updatePlayers(self.players.values())

    @rpg.command(pass_context=1, help="Reset channels!")
    async def resetchannels(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.initChannels()
        await self.bot.say("RPG channels reset")

    @rpg.command(pass_context=1, help="Reset rpg data!")
    async def resetstats(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.initRpgDB()
        await self.bot.say("RPG stats reset")

    @rpg.command(pass_context=1, help="Set rpg channel!")
    async def setchannel(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.setRPGChannel(ctx.message.server.id, ctx.message.channel.id)
        await self.bot.say("This channel is now the rpg channel for this server")
