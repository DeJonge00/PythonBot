import asyncio, datetime, discord, log, math, pickle, random, rpggame.rpgcharacter
from discord.ext import commands
from discord.ext.commands import Bot

RPGSTATSFILE = 'logs/rpgstats.txt'
RPGCHANNELID = "238995787927912449"
RPG_EMBED_COLOR = 0xFF00FF

class RPGgame:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bot.loop.create_task(self.gameloop())
        self.party = []

    async def battle1v1(self, p1, p2=rpggame.rpgcharacter.RPGCharacter("Monster", health=50)):
        battlereport = "Battle between **" + p1.name + "** (" + str(p1.health) + ") and **" + p2.name + "** (" + str(p2.health) + ")!\n"
        i = 0
        while (i<30) & (p1.health > 0) & (p2.health > 0):
            ws = random.randint(0, p1.weaponskill + p2.weaponskill)
            if (ws < p1.weaponskill):
                damage = math.floor((random.randint(100, 200) * p1.damage)/100);
                await p2.AddHealth(-1*damage)
                battlereport += "\n**" + p1.name + "** attacked for **" + str(damage) + "**"
            p3 = p1
            p1 = p2
            p2 = p3
            #print(p1.name + ": " + str(p1.health) + " | " + p2.name + " : " + str(p2.health))
            i += 1
        if(p1.health <= 0):
            battlereport += "\n\nThe battle is over, **" + p2.name + "** (" + str(p2.health) + ") laughs while walking away from **" + p1.name + "**'s corpse"
        else:
            battlereport += "\n\nThe battle lasted long, both players are exhausted. They agree on a draw *this time*\nHealthreport: **" + p1.name + "** (" + str(p1.health) + "), **" + p2.name + "** (" + str(p2.health) + ")"
        await self.bot.send_message(self.bot.get_channel(RPGCHANNELID), battlereport);

    async def gameloop(self):
        await self.bot.wait_until_ready()
        #print("Gameloop started!")
        running = True;
        await self.initialize()
        while running:
            time = datetime.datetime.utcnow()
            if time.minute%5 == 0:
                print(time)
            if time.minute == 0:
                print("Boss time!")
                self.party = []
            for u in self.bot.rpgstats:
                if u.health < u.maxhealth:
                    await u.AddHealth(10)
                if u.adventure > 0:
                    u.adventure -= 1
                    if(random.randint(0,10)<=0):
                        await self.battle1v1(u)

            endtime = datetime.datetime.utcnow()
            #print(60-(endtime).seconds)
            await asyncio.sleep(60-endtime.second)

    async def getPlayerData(self, user):
        for d in self.bot.rpgstats:
            if d.user == user:
                return d
        print("User not found: " + user.name)
        newdata = rpggame.rpgcharacter.RPGPlayer(user)
        self.bot.rpgstats.append(newdata)
        return newdata

    async def handle(self, message):
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
        with open(RPGSTATSFILE, 'wb') as fp:
            pickle.dump(self.bot.rpgstats, fp)

    #   Commands
    # {prefix}rpgadventure #
    @commands.command(pass_context=1, aliases=["rpgadv"], help="Go on an adventure!")
    async def rpgadventure(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
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
        await self.bot.say("You are now adventuring for " + str(n) + " minutes, good luck!")

    # {prefix}rpgbattle <user>
    @commands.command(pass_context=1, help="Battle a fellow discord ally to a deadly fight!")
    async def rpgbattle(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(ctx.message.mentions)<1:
            return await self.bot.say("You need to tag someone to battle with!")
        await self.battle1v1(await self.getPlayerData(ctx.message.author), p2=await self.getPlayerData(ctx.message.mentions[0]))

    # {prefix}rpgjoin
    @commands.command(pass_context=1, help="Join a raid to kill a boss!")
    async def rpgjoin(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        data = await self.getPlayerData(ctx.message.author)
        if data in self.party:
            return await self.bot.say("You are already in the boss raid party...")
        self.party.append(data)
        await self.bot.say("Prepare yourself! You and your party of " + str(len(self.party)) + " will be fighting the boss at the hour mark!")

    # {prefix}rpgparty
    @commands.command(pass_context=1, help="All players gathered to kill the boss")
    async def rpgparty(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(self.party) <= 0:
            return await self.bot.say("There is no planned boss raid, but you are welcome to start a party!")        
        embed = discord.Embed(colour=RPG_EMBED_COLOR)
        embed.set_author(name=str(self.bot.user.name), icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Boss raiding party", value=str(len(self.party)) + " adventurers", inline=False)
        m = ""
        for n in self.party:
            m += n.name + ", level " + str(await n.getLevel()) + "\n"
        embed.add_field(name="Adventurers", value=m, inline=False)
        await self.bot.say(embed=embed)

    # {prefix}rpgtop #
    @commands.command(pass_context=1, help="Show the people with the most experience!")
    async def rpgtop(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
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
        embed.set_author(name=str(self.bot.user.name), icon_url=self.bot.user.avatar_url)
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
            