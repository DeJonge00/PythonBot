import asyncio, datetime, discord, log, math, pickle, random, removeMessage, rpggame.rpgcharacter, sqlite3
from discord.ext import commands
from discord.ext.commands import Bot

RPGSTATSFILE = 'logs/rpgstats.txt'
RPGCHANNELFILE = 'logs/rpgchannel.db'
RPG_EMBED_COLOR = 0x710075

class RPGgame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bot.loop.create_task(self.gameloop())
        self.bossparties = {}

    async def battle1v1(self, channel : discord.Channel, p1 : rpggame.rpgcharacter.RPGCharacter, p2=rpggame.rpgcharacter.RPGCharacter("Monster", health=30), short=False, mockbattle=False):
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Battle", value=p1.name + " (" + str(p1.health) + ") vs " + p2.name + " (" + str(p2.health) + ")", inline=False)
        battlereport = ""
        i = 0
        h1 = p1.health
        h2 = p2.health
        while (i<30) & (p1.health > 0) & (p2.health > 0):
            ws = random.randint(0, p1.weaponskill + p2.weaponskill)
            if (ws < p1.weaponskill):
                damage = math.floor((random.randint(100, 200) * p1.damage)/100);
                await p2.addHealth(-1*damage)
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
            if isinstance(p1, rpgcharacter.RPGPlayer):
                p1.addExp(100)
            if isinstance(p2, rpgcharacter.RPGPlayer):
                p2.addExp(100)
        await self.bot.send_message(channel, embed=embed);

    async def bossbattle(self, boss=rpggame.rpgcharacter.RPGCharacter("Monster", health=250)):
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
        await self.initialize()
        while running:
            time = datetime.datetime.utcnow()
            if time.minute%5 == 0:
                print(time)
            if time.minute%15 == 0:
                try:
                    with open(RPGSTATSFILE, 'wb') as fp:
                        pickle.dump(self.bot.rpgstats, fp)
                    print("RPGStsts saved")
                except:
                    print("RPGStats saving failed")
            if time.minute == 0:
                await self.bossbattle()
                self.bossparties = {}
            for u in self.bot.rpgstats:
                if u.health < u.maxhealth:
                    await u.addHealth(10)
                if u.adventure > 0:
                    u.adventure -= 1
                    if(random.randint(0,5)<=0):
                        await self.battle1v1(u.adventurechannel, u, short=True)

            endtime = datetime.datetime.utcnow()
            #print("Sleeping for " + str(60-(endtime).second) + "s")
            await asyncio.sleep(60-endtime.second)

    async def getParty(self, serverid):
        party = self.bossparties.get(serverid)
        if party == None:
            party = set()
            self.bossparties[serverid] = party
        return party

    async def getPlayerData(self, user : discord.User):
        for d in self.bot.rpgstats:
            if d.user == user:
                return d
        print("User not found: " + user.name)
        newdata = rpggame.rpgcharacter.RPGPlayer(user)
        self.bot.rpgstats.append(newdata)
        return newdata

    async def handle(self, message : discord.Message):
        data = await self.getPlayerData(message.author)
        i = round(pow((await data.getLevel())+1, 1/3)  # levelbonus
                *max(0, min(50, (len(message.content) - 3) / 2))); # Textbonus
        await data.addExp(i)

    async def initialize(self):
        try:
            with open (RPGSTATSFILE, 'rb') as fp:
                self.bot.rpgstats = pickle.load(fp)
        except:
            print("Loading playerstats failed")
            self.bot.rpgstats = []

    async def quit(self):
        self.running = False
        #save rpgstats
        with open(RPGSTATSFILE, 'wb') as fp:
            pickle.dump(self.bot.rpgstats, fp)

    @commands.group(pass_context=1, aliases=["g"], help="'>help rpg' for full options")
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            await removeMessage.deleteMessage(self.bot, ctx)
            print("Commandnotfound")
    
    # DB commands
    @rpg.command(pass_context=1, help="Reset channels!")
    async def resetchannels(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        conn = sqlite3.connect(RPGCHANNELFILE)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS rpgchannel")
        c.execute("CREATE TABLE rpgchannel (serverID INTEGER, channelID INTEGER)")
        conn.commit()
        conn.close()
        await self.bot.say("RPG channels reset")

    @rpg.command(pass_context=1, help="Set rpg channel!")
    async def setchannel(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if(not await removeMessage.nyaCheck(self.bot, ctx)):
            return
        conn = sqlite3.connect(RPGCHANNELFILE)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO rpgchannel VALUES (" + ctx.message.server.id + ", " + ctx.message.channel.id + ")")
        t = c.fetchone()
        conn.commit()
        conn.close()
        await self.bot.say("This channel is now the rpg channel for this server")

    # {prefix}rpgadventure #
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
        data = await self.getPlayerData(ctx.message.author)
        if data.adventure > 0:
            return await self.bot.say("You are already on an adventure")
        if n<5:
            return await self.bot.say("You came back before you even went out, 0 exp earned")
        if n>120:
            return await self.bot.say("You do not have the stamina to go on that long of an adventure")
        data.adventure = n
        await self.bot.say(ctx.message.author.mention + ", you are now adventuring for " + str(n) + " minutes, good luck!")

    # {prefix}rpgbattle <user>
    @rpg.command(pass_context=1, aliases=["b"], help="Battle a fellow discord ally to a deadly fight!")
    async def battle(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)<1:
            return await self.bot.say("You need to tag someone to battle with!")
        if ctx.message.mentions[0] == ctx.message.author:
            return await self.bot.say("Suicide is never the answer :angry:")
        await self.battle1v1(ctx.message.channel, await self.getPlayerData(ctx.message.author), p2=await self.getPlayerData(ctx.message.mentions[0]), mockbattle=True)

    # {prefix}rpgstats <user>
    @rpg.command(pass_context=1, aliases=['i'], help="Show the character's status information!")
    async def info(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions)>0:
            data = await self.getPlayerData(ctx.message.mentions[0])
        else:
            data = await self.getPlayerData(ctx.message.author)
        statnames = "Username:"
        stats = data.name
        statnames += "\nExperience:"
        stats += "\n" + str(data.exp) + " (" + str(await data.getLevel()) + ")"
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

    # {prefix}rpgjoin
    @rpg.command(pass_context=1, aliases=["j"], help="Join a raid to kill a boss!")
    async def join(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        data = await self.getPlayerData(ctx.message.author)
        party = await self.getParty(ctx.message.server.id)
        if data in party:
            return await self.bot.say("You are already in the boss raid party...")
        party.add(data)
        await self.bot.say("Prepare yourself! You and your party of " + str(len(party)) + " will be fighting the boss at the hour mark!")

    # {prefix}rpgparty
    @rpg.command(pass_context=1, aliases=["p"], help="All players gathered to kill the boss")
    async def party(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        party = await self.getParty(ctx.message.server.id)
        if len(party) <= 0:
            return await self.bot.say("There is no planned boss raid, but you are welcome to start a party!")        
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.add_field(name="Boss raiding party", value=str(len(party)) + " adventurers", inline=False)
        m = ""
        for n in party:
            m += n.name + ", level " + str(await n.getLevel()) + "\n"
        embed.add_field(name="Adventurers", value=m, inline=False)
        await self.bot.say(embed=embed)

     # {prefix}rpgshop <item>
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

     # {prefix}rpgtrain
    @rpg.command(pass_context=1, aliases=["t"], help="Train your character!")
    async def train(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args)<=0:
            return print("training")
        if args[0] in ["1", "ws", "hp"]:
            return print("train health")
        if args[0] in ["2", "damage", "dam"]:
            return print("train damage")

    # {prefix}rpgtop #
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
        list = sorted(self.bot.rpgstats, key=lambda user: -1*user.exp)
        if (len(list) < (USERS_PER_PAGE*n)):
            return await self.bot.say("There are only " + str(math.ceil(len(list)/USERS_PER_PAGE)) + " pages...")
        for i in range(USERS_PER_PAGE):
            if (len(list) <= ((USERS_PER_PAGE*n)+i)):
                break
            m = list[(USERS_PER_PAGE*n)+i]
            embed.add_field(name="["+str((USERS_PER_PAGE*n)+i+1)+"] "+m.name, value=str(m.exp)+" exp\nLevel "+str(await m.getLevel()))
        await self.bot.send_message(ctx.message.channel, embed=embed)
            