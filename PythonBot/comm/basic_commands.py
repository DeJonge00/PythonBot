import asyncio, datetime, constants, discord, log, random, re, removeMessage, send_random, wikipedia, sqlite3, requests
from discord.ext import commands
from discord.ext.commands import Bot
from os import listdir
import urbandictionary as ud
from secret import secrets
from rpggame import rpgdbconnect as dbcon

TIMER = True
EMBED_COLOR = 0x008909

# Normal commands
class Basics:
    def __init__(self, my_bot):
        self.bot = my_bot
        if TIMER:
            self.bot.heresy = {}
            self.bot.nonazi = {}
            self.bot.fps = {}
            self.bot.biri = {}
            self.bot.cat = {}
            self.bot.cuddle = {}
            self.bot.ded = {}
            self.bot.nyan = {}
            self.bot.happy = {}
            self.bot.sadness = {}
            self.bot.lewd = {}
            self.bot.plsno = {}
        self.patTimes = {}

    # {prefix}60
    @commands.command(pass_context=1, help="Help get cancer out of this world!", aliases=["60"])
    async def fps(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.fps.get(ctx.message.channel.id)
            if t is not None:
                if (datetime.datetime.utcnow() - t).seconds < 60:
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.fps[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "60")

    # {prefix}biribiri
    @commands.command(pass_context=1, help="Waifu == laifu!", aliases=["biri"])
    async def biribiri(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.biri.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.biri[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "biribiri")

    # {prefix}botstats
    @commands.command(pass_context=1, help="Biri's botstats!", aliases=['botinfo'])
    async def botstats(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        embed = discord.Embed(colour=0x000000)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='Name', value=str(self.bot.user.name))
        embed.add_field(name='Id', value=str(self.bot.user.id))
        embed.add_field(name="Birthdate", value=self.bot.user.created_at.strftime("%D, %H:%M:%S"))
        embed.add_field(name='Servers', value=str(len(self.bot.servers)))
        embed.add_field(name='Lewd dm channels', value=str(len(self.bot.private_channels)))
        embed.add_field(name='Emojis', value=str(len([_ for _ in self.bot.get_all_emojis()])))
        embed.add_field(name='Fake friends', value=str(len([_ for _ in self.bot.get_all_members()])))
        embed.add_field(name='Commands', value=str(len(self.bot.commands)))
        embed.add_field(name='Owner', value='Nya#2698')
        embed.add_field(name='Landlord', value='Kappa#2915')
        embed.set_image(url=self.bot.user.avatar_url)
        return await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}cast <user>
    @commands.command(pass_context=1, help="Cast a spell!")
    async def cast(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            return await self.bot.send_message(ctx.message.channel, "{}, you cannot cast without a target...".format(ctx.message.author.name))
        return await self.bot.send_message(ctx.message.channel, "{} casted **{}** on {}.\n{}".format(ctx.message.author.name, constants.spell[random.randint(0, len(constants.spell)-1)], " ".join(args), constants.spellresult[random.randint(0, len(constants.spellresult)-1)]))
    
    # {prefix}cat
    @commands.command(pass_context=1, help="CATS!")
    async def cat(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.cat.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.cat[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "cat")

    # {prefix}compliment <user>
    @commands.command(pass_context=1, help="Give someone a compliment")
    async def compliment(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        return await send_random.string(self.bot, ctx.message.channel, constants.compliments, [" ".join(args)])
    
    # {prefix}countdown time
    @commands.command(pass_context=1, help="Tag yourself a whole bunch until the timer runs out (dm only)")
    async def countdown(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if not ctx.message.channel.is_private:
            await self.bot.say('This can only be used in private for spam reasons')
            return
        try:
            n = int(args[0])
        except ValueError:
            await self.bot.say("Thats not a number uwu")
            return
        except IndexError:
            await self.bot.say("I cannot hear you")
            return
        if n < 1:
            await self.bit.say("Lol r00d")
            return
        timers = [3600,1800,600,300,120,60,30,15,10,9,8,7,6,5,4,3,2,1]
        if n > timers[0]:
            await asyncio.sleep(n-timers[0])
            n = timers[0]
        for i in range(len(timers)):
            if n >= timers[i]:
                await self.bot.say("{}, you gotta do stuff in {} seconds!!!".format(ctx.message.author.mention, n))
                if i+1 < len(timers):
                    await asyncio.sleep((timers[i]-timers[i+1]))
                    n = timers[i+1]
                else:
                    await asyncio.sleep(n-timers[i])
                    n -= timers[i]
        await asyncio.sleep(n)
        await self.bot.say("{}, you gotta do stuff NOW!!!".format(ctx.message.author.mention))

    # {prefix}cuddle
    @commands.command(pass_context=1, help="Cuddles everywhere!")
    async def cuddle(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.cuddle.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.cuddle[ctx.message.channel.id] = datetime.datetime.utcnow()
        folder = "cuddle"
        m = await self.bot.send_file(ctx.message.channel, send_random.homedir + folder + "/" + random.choice(listdir(folder)))
        if len(ctx.message.mentions)>0:
            await self.bot.edit_message(m, new_content="Lots of cuddles for {} :heart:".format(ctx.message.mentions[0].mention))

    # {prefix}ded
    @commands.command(pass_context=1, help="Ded chat reminder!")
    async def ded(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.ded.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.ded[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "ded")

    # {prefix}delete
    @commands.command(pass_context=1, help="Delete your message automatically in a bit!", aliases=["del", "d"])
    async def delete(self, ctx, *args):
        if len(args) > 0:
            s = args[0]
            try: 
                s = float(s)
            except ValueError:
                s = 1
            await asyncio.sleep(s)
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")

    # {prefix}echo <words>
    @commands.command(pass_context=1, help="I'll be a parrot!")
    async def echo(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ctx.message.content == "":
            return await self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " b-b-baka!")
        return await self.bot.send_message(ctx.message.channel, " ".join(args))

    # {prefix}emoji <emoji>
    @commands.command(pass_context=1, help="Make big emojis")
    async def emoji(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            return await self.bot.send_message(ctx.message.channel, "I NEED MORE ARGUMENTS")

        try:
            emojiid = re.findall('\d+', ctx.message.content)[0]
        except IndexError:
            emoji = re.findall('[a-zA-Z]+', ctx.message.content)
            for e in self.bot.get_all_emojis():
                if e.name in emoji:
                    emojiid = e.id
                    break
        ext = 'gif' if requests.get('https://cdn.discordapp.com/emojis/{}.gif'.format(emojiid)).status_code == 200 else 'jpg'
        embed = discord.Embed(colour=0x000000)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://discordapp.com/api/emojis/{}.{}".format(emojiid, ext))
        return await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}emojify <words>
    @commands.command(pass_context=1, help="Use emojis to instead of ascii to spell!")
    async def emojify(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
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
        await removeMessage.deleteMessage(self.bot, ctx)
        await send_random.string(self.bot, ctx.message.channel, constants.faces)

    # {prefix}heresy
    @commands.command(pass_context=1, help="Fight the heresy!")
    async def heresy(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.heresy.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.heresy[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "heresy")

    # {prefix}happy
    @commands.command(pass_context=1, help="Awwww yeaaahhh!")
    async def happy(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.happy.get(ctx.message.channel.id)
            if not t is None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.happy[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.embeddedGif(self.bot, ctx.message.channel, 'Happinesssss', ctx.message.author.avatar_url, constants.happy_gifs)

    # {prefix}hug <person>
    @commands.command(pass_context=1, help="Give hugs!")
    async def hug(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ((ctx.message.content == "") | (ctx.message.content.lower() == ctx.message.author.name.lower()) | (ctx.message.author in ctx.message.mentions)):
            await self.bot.send_message(ctx.message.channel, ctx.messageauthor.mention + "Trying to give yourself a hug? Haha, so lonely...")
            return
        await send_random.string(self.bot, ctx.message.channel, constants.hug, [ctx.message.author.mention, " ".join(args)])

     # {prefix}kick
    @commands.command(pass_context=1, help="Fake kick someone")
    async def kick(self, ctx, *args):
        if len(ctx.message.mentions) > 0:
            await self.bot.send_typing(ctx.message.channel)
            if (ctx.message.author == ctx.message.mentions[0]):
                await self.bot.send_message(ctx.message.channel, "You could just leave yourself if you want to go :thinking:")
                return
            embed = discord.Embed(colour=0xFF0000)
            embed.add_field(name="User left", value="\"" + ctx.message.mentions[0].name + "\" just left. Byebye, you will not be missed!")
            m = await self.bot.say(embed=embed)

    # {prefix}kill <person>
    @commands.command(pass_context=1, help="Wish someone a happy death! (is a bit explicit)")
    async def kill(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ((ctx.message.content == "") | (ctx.message.content.lower() == ctx.message.author.name.lower()) | (ctx.message.author in ctx.message.mentions)):
            return await self.bot.send_message(ctx.message.channel, "Suicide is not the answer, 42 is")
        await send_random.string(self.bot, ctx.message.channel, constants.kill, [" ".join(args)])

    # {prefix}lenny <words>
    @commands.command(pass_context=1, help="( ͡° ͜ʖ ͡°)!")
    async def lenny(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        await self.bot.send_message(ctx.message.channel, " ".join(args) + " ( ͡° ͜ʖ ͡°)")

    # {prefix}lewd
    @commands.command(pass_context=1, help="LLEEEEEEEEWWDD!!!")
    async def lewd(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.lewd.get(ctx.message.channel.id)
            if not t is None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.lewd[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.embeddedGif(self.bot, ctx.message.channel, 'Leeeeeewwwdd!', ctx.message.author.avatar_url, constants.lewd_gifs)

    # {prefix}lottery <minutes> <description>
    @commands.command(pass_context=1, help="Set up a lottery!")
    async def lottery(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) < 1:
            desc = "Something something LOTTERY!!"
        else:
            desc = " ".join(args)
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        mess = desc + "\nAdd a 👍 reaction to participate!"
        embed.add_field(name="Be in it to win it!", value=mess)
        m = await self.bot.say(embed=embed)
        lotterylist = set()
        await self.bot.add_reaction(m, "👍")
        i = self.bot.user
        while not (i == ctx.message.author):
            r = await self.bot.wait_for_reaction(['👍'], message=m)
            if not r.user.bot:
                lotterylist.add(r.user)
            i = r.user

        # Select winner
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        mess = "Out of the " + str(len(lotterylist)) + " participants, " + random.sample(lotterylist, 1)[0].name + " is the lucky winner!"
        embed.add_field(name="Lottery winner", value=mess)
        await self.bot.say(embed=embed)

    # {prefix}nonazi
    @commands.command(pass_context=1, help="Try to persuade Lizzy with anti-nazi-propaganda!")
    async def nonazi(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.nonazi.get(ctx.message.channel.id)
            if t != None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.nonazi[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.file(self.bot, ctx.message.channel, "nonazi")

    # {prefix}nyan
    @commands.command(pass_context=1, help="Nyanyanyanyanyanyanyanyanya!")
    async def nyan(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.nyan.get(ctx.message.channel.id)
            if not t is None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.nyan[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.embeddedGif(self.bot, ctx.message.channel, 'Nyan', ctx.message.author.avatar_url, constants.nyan_gifs)

    # # {prefix}nyanya
    # @commands.command(pass_context=1, help="Nyanyanyanyanyanyanyanyanya!")
    # async def nyanya(self, ctx, *args):
    #     await removeMessage.deleteMessage(self.bot, ctx)
    #     if TIMER:
    #         t = self.bot.nyan.get(ctx.message.channel.id)
    #         if not t is None:
    #             if (datetime.datetime.utcnow() - t).seconds < (60):
    #                 return
    #         await self.bot.send_typing(ctx.message.channel)
    #         self.bot.nyan[ctx.message.channel.id] = datetime.datetime.utcnow()
    #
    #     embed = discord.Embed(colour=0x00969b)
    #     embed.set_author(name='Catgirls for you <3', icon_url=ctx.message.author.avatar_url)
    #     embed.set_image(url = [x for x in requests.get('https://weeb.sh/').text.split('"') if 'images' in x][1])
    #     embed.set_footer(text='see weeb.sh for more')
    #     await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}pat <name>
    @commands.command(pass_context=1, help="PAT ALL THE THINGS!")
    async def pat(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions) <= 0:
            return await self.bot.say(ctx.message.author.mention + " You cant pat air lmao")
        if ctx.message.mentions[0].id == ctx.message.author.id:
            return await self.bot.say(ctx.message.author.mention + " One does not simply pat ones own head")
        
        time = datetime.datetime.utcnow()
        t = self.patTimes.get(ctx.message.author.id)

        if (t != None):
            if ((time-t).total_seconds() < 60):
                await self.bot.say(ctx.message.author.mention + " Not so fast, b-b-baka!")
                return
        self.patTimes[ctx.message.author.id] = time

        n = dbcon.incrementPats(ctx.message.author.id, ctx.message.mentions[0].id)
        s = '' if n == 1 else 's'
        m = "{} has pat {} {} time{} now".format(ctx.message.author.mention, ctx.message.mentions[0].mention, n, s)
        if n%100==0:
            m += "\nWoooooaaaaahh LEGENDARY!!!"
        elif n%25==0:
            m += "\nWow, that is going somewhere!"
        elif n%10==0:
            m += "\nSugoi!"
        await self.bot.say(m);

    # {prefix}plsno
    @commands.command(pass_context=1, help="Nonononononono!")
    async def plsno(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.plsno.get(ctx.message.channel.id)
            if not t is None:
                if (datetime.datetime.utcnow() - t).seconds < (60):
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.plsno[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.embeddedGif(self.bot, ctx.message.channel, 'Pls no', ctx.message.author.avatar_url, constants.plsno_gifs)

    # {prefix}role <name>
    @commands.command(pass_context=1, help="Add or remove roles!")
    async def role(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(args) <= 0:
            await self.bot.say("Usage: {}role <rolename without spaces> [\{user\}]".format(constants.prefix))
            return
        else:
            rolename = args[0].lower()
        authorhasperms = ctx.message.channel.permissions_for(ctx.message.author).manage_roles or (ctx.message.server.owner.id == ctx.message.author.id)
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            if not authorhasperms:
                await self.bot.send_message(ctx.message.channel, "You do not have the permissions to give other people roles")
                return
            user = ctx.message.mentions[0]
        if not (authorhasperms or rolename in ['nsfw', 'muted']):
            await self.bot.say("You lack the permissions for that")
            return
        role = None
        for r in ctx.message.server.roles:
            if r.name.lower().replace(' ', '') == rolename:
                role = r
                break
        if not role:
            await self.bot.send_message(ctx.message.channel, "Role {} not found".format(role))
            return
        try:
            if role in ctx.message.author.roles:
                await self.bot.remove_roles(user, role)
                await self.bot.send_message(ctx.message.channel, "Role {} succesfully removed".format(role.name))
                return
            else:
                await self.bot.add_roles(user, role)
                await self.bot.send_message(ctx.message.channel, "Role {} succesfully added".format(role.name))
                return
        except discord.Forbidden:
            await self.bot.send_message(ctx.message.channel, "I dont have the perms for that sadly...")
            return

    # {prefix}sadness
    @commands.command(pass_context=1, help="Cri!")
    async def sadness(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if TIMER:
            t = self.bot.sadness.get(ctx.message.channel.id)
            if not t is None:
                if (datetime.datetime.utcnow() - t).seconds < 60:
                    return
            await self.bot.send_typing(ctx.message.channel)
            self.bot.sadness[ctx.message.channel.id] = datetime.datetime.utcnow()
        await send_random.embeddedGif(self.bot, ctx.message.channel, 'Sadnessss', ctx.message.author.avatar_url, constants.sad_gifs)

    # {prefix}serverinfo
    @commands.command(pass_context=1, help="Get the server's information!")
    async def serverinfo(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if ctx.message.channel.is_private:
            await self.bot.say('That cannot be done in private')
            return
        server = ctx.message.server
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=server.name, icon_url=ctx.message.author.avatar_url)
        if server.icon != None:
            embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Server ID", value=server.id)
        embed.add_field(name="Creation date", value=server.created_at)
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Members", value=server.member_count)
        embed.add_field(name="Owner", value=server.owner.display_name)
        embed.add_field(name="Custom Emoji", value=len(server.emojis))
        embed.add_field(name="Roles", value=len(server.roles))
        embed.add_field(name="Channels", value=len(server.channels))
        if len(server.features) > 0:
            f = ""
            for feat in server.features:
                f += "{}\n".format(feat)
            embed.add_field(name="Features", value=f)
        if server.splash != None:
            embed.add_field(name="Splash", value=server.splash)
        await self.bot.say(embed=embed)

    # {prefix}urban <query>
    @commands.command(pass_context=1, help="Search the totally official wiki!", aliases=["ud", "urbandictionary"])
    async def urban(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        q = " ".join(args)
        if q == "":
            await self.bot.send_message(ctx.message.channel, "...")
            return
        embed = discord.Embed(colour=0x0000FF)
        embed.add_field(name="Urban Dictionary Query", value=q)
        try:
            r = ud.define(q)[0]
            embed.add_field(name="Definition", value=r.definition, inline=False)
            embed.add_field(name="Example", value=r.example)
            embed.add_field(name="👍", value=r.upvotes)
            embed.add_field(name="👎", value=r.downvotes)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            return
        except IndexError:
            embed.add_field(name="Definition", value="ERROR ERROR ... CANT HANDLE AWESOMENESS LEVEL")
            await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}userinfo <user>
    @commands.command(pass_context=1, help="Get a user's information!", aliases=["user", "info"])
    async def userinfo(self, ctx, *args):
        await removeMessage.deleteMessage(self.bot, ctx)
        if len(ctx.message.mentions) <= 0:
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
        await removeMessage.deleteMessage(self.bot, ctx)
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