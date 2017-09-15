import asyncio, datetime, constants, discord, log, random, responses, send_random, wikipedia
from discord.ext import commands
from discord.ext.commands import Bot
from urbanpyctionary.client import Client

# Normal commands
class Basics:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.bot.fps = self.bot.biri = self.bot.cat = self.bot.cuddle = datetime.datetime.utcnow()

    # {prefix}60
    @commands.command(pass_context=1, help="\n\tHelp get cancer out of this world!", aliases=["60"])
    async def fps(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        if (datetime.datetime.utcnow() - self.bot.fps).seconds < (2*60):
            return
        await self.bot.send_typing(ctx.message.channel)
        self.bot.fps = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "60")

   # # {prefix}big <emoji>
   # @commands.command(pass_context=1, help="Enlarge an emoji")
   # async def biribiri(self, ctx, *args):
   #     try:
   #         await self.bot.delete_message(ctx.message)
   #     except discord.Forbidden:
   #         print(ctx.message.server + " | No permission to delete messages")
   #


    # {prefix}biribiri
    @commands.command(pass_context=1, help="Waifu == laifu!", aliases=["biri"])
    async def biribiri(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        if (datetime.datetime.utcnow() - self.bot.biri).seconds < (2*60):
            return
        await self.bot.send_typing(ctx.message.channel)
        self.bot.biri = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "biribiri")
    
    # {prefix}cast <user>
    @commands.command(pass_context=1, help="Cast a spell!")
    async def cast(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(args) <= 0:
            return await self.bot.send_message(ctx.message.channel, ctx.message.author.name + ", you cannot cast without a target...")
        return await self.bot.send_message(ctx.message.channel, ctx.message.author.name + " casted **" + responses.spell[randint(0, len(responses.spell)-1)] + "** on " + " ".join(args) + ".\n" +  responses.spellresult[randint(0, len(responses.spellresult)-1)])

    # {prefix}cat
    @commands.command(pass_context=1, help="CATS!")
    async def cat(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden as e:
            print(ctx.message.server + " | No permission to delete messages")
        if (datetime.datetime.utcnow() - self.bot.cat).seconds < (2*60):
            return
        await self.bot.send_typing(ctx.message.channel)
        self.bot.cat = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "cat")
    
    # {prefix}compliment <user>
    @commands.command(pass_context=1, help="Give someone a compliment")
    async def compliment(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        return await send_random.string(self.bot, ctx.message.channel, responses.compliments, [" ".join(args)])
    
    # {prefix}cuddle
    @commands.command(pass_context=1, help="Cuddles everywhere!")
    async def cuddle(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        if (datetime.datetime.utcnow() - self.bot.cuddle).seconds < (2*60):
            return
        await self.bot.send_typing(ctx.message.channel)
        self.bot.cuddle = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "cuddle")

    # {prefix}ded
    @commands.command(pass_context=1, help="Ded chat reminder!")
    async def ded(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        await send_random.file(self.bot, ctx.message.channel, "ded")

    # {prefix}delete
    @commands.command(pass_context=1, help="Delete your message automatically in a bit!", aliases=["del", "d"])
    async def delete(self, ctx, *args):
        s = args[0]
        try: 
            int(s)
        except ValueError:
            s = 20
        s *= 100
        asyncio.sleep(s)
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")

    # {prefix}echo <words>
    @commands.command(pass_context=1, help="I'll be a parrot!")
    async def echo(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if ctx.message.content == "":
            return await self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " b-b-baka!")
        return await self.bot.send_message(ctx.message.channel, " ".join(args))

    # {prefix}emojify <words>
    @commands.command(pass_context=1, help="Use emojis to instead of ascii to spell!")
    async def emojify(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        text = " ".join(args).lower()
        etext = ""
        for c in text:
            if (c.isalpha()) & (c != " "):
                etext += ":regional_indicator_" + c + ":"
            else:
                if c == "?":
                    etext += ":question:"
                else:
                    if c == "!":
                        etext += ":exclamation:"
                    else:
                        etext += c

        return await self.bot.send_message(ctx.message.channel, etext)

    # {prefix}face
    @commands.command(pass_context=1, help="Make a random face!")
    async def face(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        await send_random.string(self.bot, ctx.message.channel, responses.faces)

    # {prefix}hug <person>
    @commands.command(pass_context=1, help="Give hugs!")
    async def hug(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if ((ctx.message.content == "") | (ctx.message.content.lower() == ctx.message.author.name.lower()) | (ctx.message.author in ctx.message.mentions)):
            return await self.bot.send_message(ctx.message.channel, "Trying to give yourself a hug? Haha, so lonely...")
        await send_random.string(self.bot, ctx.message.channel, responses.hug, [ctx.message.author.mention, " ".join(args)])

     # {prefix}kick
    @commands.command(pass_context=1, help="kick someone for funzies")
    async def kick(self, ctx, *args):
        if len(ctx.message.mentions) > 0:
            await self.bot.send_typing(ctx.message.channel)
            if (ctx.message.author == ctx.message.mentions[0]):
                return await self.bot.send_message(ctx.message.channel, "You could just leave yourself if you want to go :thinking:")
            embed = discord.Embed(colour=0xFF0000)
            embed.add_field(name=" <:cate:290483030227812353> <:cate:290483030227812353> User left", value="\"" + ctx.message.mentions[0].name + "\" just left. Byebye, you will not be missed! <:cate:290483030227812353> <:cate:290483030227812353>")
            m = await self.bot.say(embed=embed)

    # {prefix}kill <person>
    @commands.command(pass_context=1, help="Wish someone a happy death!")
    async def kill(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if ((ctx.message.content == "") | (ctx.message.content.lower() == ctx.message.author.name.lower()) | (ctx.message.author in ctx.message.mentions)):
            return await self.bot.send_message(ctx.message.channel, "Suicide is not the answer, 42 is")
        await send_random.string(self.bot, ctx.message.channel, responses.kill, [" ".join(args)])

    # {prefix}lenny <words>
    @commands.command(pass_context=1, help="( ͡° ͜ʖ ͡°)!")
    async def lenny(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        return await self.bot.send_message(ctx.message.channel, " ".join(args) + " ( ͡° ͜ʖ ͡°)")

    # {prefix}lottery <minutes> <description>
    @commands.command(pass_context=1, help="Set up a lottery!")
    async def lottery(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(args)<1:
            desc = "Something something LOTTERY!!"
        else:
            desc = " ".join(args)
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        mess = desc + "\nAdd a 👍 reaction to participate!"
        embed.add_field(name="Be in it to win it!", value=mess)
        m = await self.bot.say(embed=embed)
        lotterylist = []
        await self.bot.add_reaction(m, "👍")
        i = self.bot.user
        while not (i == ctx.message.author):
            r = await self.bot.wait_for_reaction(['👍'], message=m)
            if not ((self.bot.user == r.user) | (r.user.id in lotterylist)):
                lotterylist.append(r.user)
            i = r.user
        # Select winner
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        mess = "Out of the " + str(len(lotterylist)) + " participants, " + random.choice(lotterylist).name + " is the lucky winner!"
        embed.add_field(name="Lottery winner", value=mess)
        await self.bot.say(embed=embed)

    # {prefix}role <name>
    @commands.command(pass_context=1, help="Add or remove roles!")
    async def role(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(args)<=0:
            return await self.bot.say("Usage: >role <role> <user>")
        else:
            rolename = args[0]
        if len(ctx.message.mentions)<=0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        if (ctx.message.channel.permissions_for(ctx.message.author).manage_roles) | ((ctx.message.server.id == constants.NINECHATid) & (rolename in ['Muted', 'nsfw', '1st Anniversary'])):
            role = None
            for r in ctx.message.server.roles:
                if r.name == rolename:
                    role = r
            if role != None:
                try:
                    if role in ctx.message.author.roles:
                        await self.bot.remove_roles(user, role)
                        return await self.bot.send_message(ctx.message.channel, "Role " + role.name + " succesfully removed")
                    else:
                        await self.bot.add_roles(user, role)
                        return await self.bot.send_message(ctx.message.channel, "Role " + role.name + " succesfully added")
                except discord.Forbidden:
                        return await self.bot.send_message(ctx.message.channel, "I dont have the perms for that sadly...")
            else:
                return await self.bot.send_message(ctx.message.channel, "Role not found (it's case sensitive)")
        else:
            return await self.bot.say("You lack the permissions for that")

    # {prefix}urban <query>
    @commands.command(pass_context=1, help="Search the totally official wiki!", aliases=["ud", "urbandictionary"])
    async def urban(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        q = " ".join(args)
        if q == "":
            return await self.bot.send_message(ctx.message.channel, "...")
        embed = discord.Embed(colour=0x0000FF)
        embed.add_field(name="Urban Dictionary Query", value=q)
        try:
            c = Client(API_key = "D00sbvewComshcNG8qlTT1U7KqVPp1RG33njsnmL9HJFCtgFF8")
            r = c.get(q)
            embed.add_field(name="Definition", value=r[1].definition, inline=False)
            embed.add_field(name="Author", value=r[1].author)
            embed.add_field(name="👍", value=r[1].thumbs_up)
            embed.add_field(name="👎", value=r[1].thumbs_down)
            return await self.bot.send_message(ctx.message.channel, embed=embed)
        except Exception as e:
            embed.add_field(name="Definition", value="ERROR ERROR ... CANT HANDLE AWESOMENESS LEVEL")
            return await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}userinfo <query>
    @commands.command(pass_context=1, help="Get a user's information!", aliases=["user"])
    async def userinfo(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        if len(ctx.message.mentions)<=0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]

        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=str(user.name), icon_url=user.avatar_url)

        if user.bot:
            botv = "Yes"
        else:
            botv = "No"
        embed.add_field(name="Bot", value=botv)
        if user.nick:
            nn = user.nick
        else:
            nn = "None"
        embed.add_field(name="Nickname", value=nn)
        embed.add_field(name="Id", value=user.id)
        embed.add_field(name="Discriminator", value=user.discriminator)
        embed.add_field(name="Status", value=user.status.name)
        if user.game:
            game = str(user.game)
        else:
            game = "Nothing"
        embed.add_field(name="Playing", value=game)
        embed.add_field(name="Joined date", value=user.joined_at.strftime("%D, %H:%M:%S"))
        m = "everyone"
        for r in range(1,len(user.roles)):
            m += "\n" + user.roles[r].name
        embed.add_field(name="Roles", value = m)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}wikipedia <query>
    @commands.command(pass_context=1, help="Search the wiki!", aliases=["wiki"])
    async def wikipedia(self, ctx, *args):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        await self.bot.send_typing(ctx.message.channel)
        q = " ".join(args)
        if q == "":
            return await self.bot.send_message(ctx.message.channel, "...")
        embed = discord.Embed(colour=0x00FF00)
        try:
            s = wikipedia.summary(q, sentences=2)
            embed.add_field(name="Query: " + q, value=s)
            return await self.bot.send_message(ctx.message.channel, embed=embed)
        except Exception as e:
            embed.add_field(name="Query: " + q, value="There are too much answers to give you the correct one...")
            return await self.bot.send_message(ctx.message.channel, embed=embed)