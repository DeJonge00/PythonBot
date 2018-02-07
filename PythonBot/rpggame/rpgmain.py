import asyncio, datetime, secret.constants as constants, discord, log, math, pickle, random, removeMessage, rpggame.rpgcharacter as rpgchar, rpggame.rpgdbconnect as dbcon, sqlite3
from discord.ext import commands
from discord.ext.commands import Bot

RPGSTATSFILE = 'logs/rpgstats.txt'
RPG_EMBED_COLOR = 0x710075
BATTLETURNS = 30

class RPGgame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bossparties = {}
        self.players = {}
        self.bot.loop.create_task(self.gameloop())

    async def battle1v1(self, channel : discord.Channel, p1 : rpgchar.RPGCharacter, p2=rpgchar.RPGMonster(), short=False, mockbattle=False):
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Battle", value=p1.name + " (" + str(p1.health) + ") vs " + p2.name + " (" + str(p2.health) + ")", inline=False)
        battlereport = ""
        i = 0
        h1 = p1.health
        h2 = p2.health
        while (i<BATTLETURNS) & (p1.health > 0) & (p2.health > 0):
            ws = random.randint(0, p1.weaponskill + p2.weaponskill)
            if (ws < p1.weaponskill):
                damage = math.floor((random.randint(100, 200) * p1.damage)/100);
                p2.addHealth(-1*damage)
                battlereport += "\n**" + p1.name + "** attacked for **" + str(damage) + "**"
            p3 = p1
            p1 = p2
            p2 = p3
            #print(p1.name + ": " + str(p1.health) + " | " + p2.name + " : " + str(p2.health))
            i += 1
        
        if short:
            if (i%2)==1:
                p3 = p1
                p1 = p2
                p2 = p3
            shortreport = p1.name + " did " + str(h2 - p2.health) + " damage while\n" + p2.name + " did " + str(h1 - p1.health) + " damage"
            embed.add_field(name="Battlereport", value=shortreport, inline=False)
        else:
            embed.add_field(name="Battlereport", value=battlereport, inline=False)
        if(p1.health <= 0):
            embed.add_field(name="Result", value=p2.name + " (" + str(p2.health) + ") laughs while walking away from " + p1.name + "'s corpse", inline=False)
        else:
            embed.add_field(name="Result", value="The battle lasted long, both players are exhausted.\nThey agree on a draw this time", inline=False)
            embed.add_field(name="Healthreport", value=p1.name + " (" + str(p1.health) + ")\n" + p2.name + " (" + str(p2.health) + ")", inline=False)
        if mockbattle:
            p1.health = h1
            p2.health = h2
        else:
            if isinstance(p1, rpgchar.RPGPlayer):
                p1.addExp(100)
            if isinstance(p2, rpgchar.RPGPlayer):
                p2.addExp(100)
        await self.bot.send_message(channel, embed=embed);

    async def bossbattle(self, boss=rpgchar.RPGMonster(name="Monster", health=250)):
        print("Boss time!")
        for serverid in self.bossparties:
            party = self.bossparties.get(serverid)
            if len(party) > 0:
                conn = sqlite3.connect(RPGCHANNELFILE)
                c = conn.cursor()
                c.execute("SELECT channelID FROM rpgchannel WHERE serverID=" + serverid)
                t = c.fetchone()
                conn.commit()
                conn.close()
                if t==None:
                    print("Channel not specified for server")
                    return
                channel = self.bot.get_channel(str(t[0]))
                await self.bot.send_message(channel, "Leeeetttssss dduuuuuueeeelllll!!!")

    async def gameloop(self):
        await self.bot.wait_until_ready()
        print("RPG Gameloop started!")
        running = True;
        while running:
            time = datetime.datetime.utcnow()
            if time.minute%5 == 0:
                print(time)
            if time.minute%15 == 0:
                p = self.players.values()
                if len(p) > 0:
                    dbcon.updatePlayers(p)
                    l = list(self.players.keys())
                    for i in l:
                        if self.players.get(i).adventuretime <= 0:
                            self.players.pop(i)
                print("Players saved")
            if time.minute == 0:
                await self.bossbattle()
                self.bossparties = {}
            for u in list(self.players.values()):
                if u.health < u.maxhealth:
                    u.addHealth(10)
                if u.adventuretime > 0:
                    u.adventuretime -= 1
                    c = self.bot.get_channel(str(u.adventurechannel))
                    if c != None:
                        if(random.randint(0,5)<=0): 
                            await self.battle1v1(c, u, short=True)

            endtime = datetime.datetime.utcnow()
            #print("Sleeping for " + str(60-(endtime).second) + "s")
            await asyncio.sleep(60-endtime.second)

    def getParty(self, serverid):
        party = self.bossparties.get(serverid)
        if party == None:
            party = set()
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
        i = round(pow((data.getLevel())+1, 1/3)  # levelbonus
                *max(0, min(50, (len(message.content) - 3) / 2))); # Textbonus
        data.addExp(i)

    async def quit(self):
        self.running = False
        #save rpgstats
        dbcon.updatePlayers(self.players.values())
        print("RPGStats saved")

    @commands.group(pass_context=1, aliases=["g"], help="'>help rpg' for full options")
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            await self.bot.say("Use '>help rpg' for all the rpg commands")
    
    @rpg.command(pass_context=1, help="Reset channels!")
    async def updatedb(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx, istyping=False)
        if not(ctx.message.author.id==constants.NYAid):
            await self.bot.say("Hahahaha, no")
            return
        dbcon.updatePlayers(self.players.values())

    # DB commands
    @rpg.command(pass_context=1, help="Reset channels!")
    async def resetchannels(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        dbcon.initChannels()
        await self.bot.say("RPG channels reset")

    @rpg.command(pass_context=1, help="Reset rpg data!")
    async def resetstats(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        dbcon.initDB()
        await self.bot.say("RPG stats reset")

    @rpg.command(pass_context=1, help="Set rpg channel!")
    async def setchannel(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        dbcon.setChannel(ctx.message.server.id, ctx.message.channel.id)
        await self.bot.say("This channel is now the rpg channel for this server")

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
        if data.adventuretime > 0:
            await self.bot.say("You are already on an adventure")
            return
        if n<5:
            await self.bot.say("You came back before you even went out, 0 exp earned")
            return
        if n>120:
            await self.bot.say("You do not have the stamina to go on that long of an adventure")
            return
        data.setAdventure(n, ctx.message.channel.id)
        await self.bot.say(ctx.message.author.mention + ", you are now adventuring for " + str(n) + " minutes, good luck!")

    # {prefix}rpg battle <user>
    @rpg.command(pass_context=1, aliases=["b"], help="Battle a fellow discord ally to a deadly fight!")
    async def battle(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)<1:
            return await self.bot.say("You need to tag someone to battle with!")
        if ctx.message.mentions[0] == ctx.message.author:
            return await self.bot.say("Suicide is never the answer :angry:")
        await self.battle1v1(ctx.message.channel, self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name), p2=self.getPlayerData(ctx.message.mentions[0], name=ctx.message.mentions[0].display_name), mockbattle=True)

    # {prefix}rpg info <user>
    @rpg.command(pass_context=1, aliases=['i', 'stats'], help="Show the character's status information!")
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
        elif data.adventuretime > 0:
            stats += "\nAdventuring for " + str(data.adventuretime) + "m"
        else:
            stats += "\nAlive"
        statnames += "\nExperience:"
        stats += "\n" + str(data.exp) + " (" + str(data.getLevel()) + ")"
        statnames += "\nHealth:"
        stats += "\n" + str(data.health) + "/" + str(data.maxhealth)
        statnames += "\nDamage:"
        stats += "\n" + str(data.damage)
        statnames += "\nWeaponskill:"
        stats += "\n" + str(data.weaponskill)

        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Statname", value=statnames)
        embed.add_field(name="Stats", value=stats)
        await self.bot.say(embed=embed)

    # {prefix}rpg join
    @rpg.command(pass_context=1, aliases=["j"], help="Join a raid to kill a boss!")
    async def join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = self.getPlayerData(ctx.message.author, name=ctx.message.author.display_name)
        party = self.getParty(ctx.message.server.id)
        if data in party:
            return await self.bot.say("You are already in the boss raid party...")
        party.add(data)
        await self.bot.say("Prepare yourself! You and your party of " + str(len(party)) + " will be fighting the boss at the hour mark!")

    # {prefix}rpg party
    @rpg.command(pass_context=1, aliases=["p"], help="All players gathered to kill the boss")
    async def party(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        party = self.getParty(ctx.message.server.id)
        if len(party) <= 0:
            return await self.bot.say("There is no planned boss raid, but you are welcome to start a party!")        
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Boss raiding party", value=str(len(party)) + " adventurers", inline=False)
        m = ""
        for n in party:
            member = ctx.message.server.get_member(str(n.userid))
            m += member.display_name + ", level " + str(n.getLevel()) + "\n"
        embed.add_field(name="Adventurers", value=m, inline=False)
        await self.bot.say(embed=embed)

     # {prefix}rpg shop <item>
    @rpg.command(pass_context=1, aliases=["s"], help="Shop for valuable items!")
    async def shop(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args)<=0:
            return print("shop inventory")
        if args[0] in ["1", "health", "hp"]:
            return print("buy health")
        if args[0] in ["2", "damage", "dam"]:
            return print("buy damage")
        return print("Item " + args[0] + " not found") 

     # {prefix}rpg train
    @rpg.command(pass_context=1, aliases=["t"], help="Train your character!")
    async def train(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args)<=0:
            return print("training")
        if args[0] in ["1", "health", "hp"]:
            return print("train health")
        if args[0] in ["2", "damage", "dam", "s", "strength"]:
            return print("train damage")

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
        USERS_PER_PAGE = 12
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="RPG top players", value="Page " + str(n+1), inline=False)
        list = dbcon.getTopPlayers()
        print(len(list))
        if (len(list) < (USERS_PER_PAGE*n)):
            return await self.bot.say("There are only " + str(math.ceil(len(list)/USERS_PER_PAGE)) + " pages...")
        end = (USERS_PER_PAGE*(n+1))
        if end > len(list):
            end = len(list)
        nums = ""
        i = (USERS_PER_PAGE*n)
        members = ""
        exp = ""
        for m in list[i:end]:
            i += 1
            try:
                name = ctx.message.server.get_member(str(m[0])).display_name
            except AttributeError:
                name = "id" + str(m[0])
            nums += str(i) + "\n"
            members += name + "\n"
            exp += str(m[1]) + "exp, L" + str(rpgchar.getLevelByExp(m[1])) + "\n"
        embed.add_field(name="Rank", value=nums)
        embed.add_field(name="Player", value=members)
        embed.add_field(name="Exp, level", value=exp)
        await self.bot.send_message(ctx.message.channel, embed=embed)
            