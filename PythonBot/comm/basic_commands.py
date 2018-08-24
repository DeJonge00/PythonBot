import asyncio
import constants
import datetime
import discord
import random
import re
import requests
import send_random
import wikipedia
from discord.ext import commands

from rpggame import rpgdbconnect as dbcon
from secret.secrets import prefix

EMBED_COLOR = 0x008909


# Normal commands
class Basics:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.patTimes = {}

    # {prefix}botstats
    @commands.command(pass_context=1, help="Biri's botstats!", aliases=['botinfo'])
    async def botstats(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='botstats'):
            return
        embed = discord.Embed(colour=0x000000)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='Profile', value=str(self.bot.user.mention))
        embed.add_field(name='Name', value=str(self.bot.user))
        embed.add_field(name='Id', value=str(self.bot.user.id))
        embed.add_field(name="Birthdate", value=self.bot.user.created_at.strftime("%D, %H:%M:%S"))
        embed.add_field(name='Servers', value=str(len(self.bot.servers)))
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
        if not await self.bot.pre_command(message=ctx.message, command='cast'):
            return

        if len(args) <= 0:
            await self.bot.say("{}, you cannot cast without a target...".format(ctx.message.author.name))

        target = ' '.join(args)
        caster = ctx.message.author.name
        spell = random.choice(constants.spell)
        result = random.choice(constants.spellresult)

        await self.bot.say("{} casted **{}** on {}.\n{}".format(caster, spell, target, result))

    # {prefix}compliment <user>
    @commands.command(pass_context=1, help="Give someone a compliment")
    async def compliment(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='compliment'):
            return
        try:
            target = await self.bot.get_member_from_message(message=ctx.message, args=args, in_text=True)
        except ValueError:
            return
        await self.bot.say(random.choice(constants.compliments).format(u=[target.mention]))

    # {prefix}countdown time
    @commands.command(pass_context=1, help="Tag yourself a whole bunch until the timer runs out (dm only)")
    async def countdown(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='countdown', must_be_private=True):
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
            await self.bot.say("Lol r00d")
            return

        timers = [3600, 1800, 600, 300, 120, 60, 30, 15, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        if n > timers[0]:
            await asyncio.sleep(n - timers[0])
            n = timers[0]
        for i in range(len(timers)):
            if n >= timers[i]:
                await self.bot.say("{}, you gotta do stuff in {} seconds!!!".format(ctx.message.author.mention, n))
                if i + 1 < len(timers):
                    await asyncio.sleep((timers[i] - timers[i + 1]))
                    n = timers[i + 1]
                else:
                    await asyncio.sleep(n - timers[i])
                    n -= timers[i]
        await asyncio.sleep(n)
        await self.bot.say("{}, you gotta do stuff NOW!!!".format(ctx.message.author.mention))

    # {prefix}delete
    @commands.command(pass_context=1, help="Delete your message automatically in a bit!", aliases=["del", "d"])
    async def delete(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='botstats', is_typing=False,
                                          delete_message=False):
            return
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
            print(self.bot.prep_str_for_print(ctx.message.server.name) + " | No permission to delete messages")

    # {prefix}echo <words>
    @commands.command(pass_context=1, help="I'll be a parrot!")
    async def echo(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='echo'):
            return

        if len(args) > 0:
            await self.bot.send_message(ctx.message.channel, " ".join(args))
            return

        if len(ctx.message.attachments) > 0:
            embed = discord.Embed(colour=0x000000)
            embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
            embed.set_image(url=ctx.message.attachments[0].get('url'))
            await self.bot.send_message(ctx.message.channel, embed=embed)
            return
        await self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " b-b-baka!")

    # {prefix}emoji <emoji>
    @commands.command(pass_context=1, help="Make big emojis")
    async def emoji(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='emoji'):
            return
        if len(args) <= 0:
            return await self.bot.send_message(ctx.message.channel, "I NEED MORE ARGUMENTS")

        emojiid = None
        try:
            emojiid = re.findall('\d+', ctx.message.content)[0]
        except IndexError:
            emoji = re.findall('[a-zA-Z]+', ctx.message.content)
            for e in self.bot.get_all_emojis():
                if e.name in emoji:
                    emojiid = e.id
                    break
        if not emojiid:
            await self.bot.say('Sorry, emoji not found...')
            return
        ext = 'gif' if requests.get(
            'https://cdn.discordapp.com/emojis/{}.gif'.format(emojiid)).status_code == 200 else 'jpg'
        embed = discord.Embed(colour=0x000000)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://discordapp.com/api/emojis/{}.{}".format(emojiid, ext))
        return await self.bot.send_message(ctx.message.channel, embed=embed)

    # {prefix}emojify <words>
    @commands.command(pass_context=1, help="Use emojis to instead of ascii to spell!")
    async def emojify(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='emojify'):
            return
        text = " ".join(args).lower()
        if not text:
            await self.bot.say('Please give me a string to emojify...')
            return
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
        if not await self.bot.pre_command(message=ctx.message, command='face'):
            return
        await self.bot.say(random.choice(constants.faces))

    # {prefix}hug <person>
    @commands.command(pass_context=1, help="Give hugs!")
    async def hug(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='hug'):
            return
        try:
            target = await self.bot.get_member_from_message(ctx.message, args, in_text=True)
        except ValueError:
            return
        if target == ctx.message.author:
            await self.bot.say(ctx.message.author.mention + "Trying to give yourself a hug? Haha, so lonely...")
            return

        await self.bot.say(random.choice(constants.hug).format(u=[ctx.message.author.mention, target.mention]))

    # {prefix}hype
    @commands.command(pass_context=1, help="Hype everyone with random emoji!")
    async def hype(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='hype'):
            return
        if ctx.message.channel.is_private:
            await self.bot.say('I can only send emoji in servers')
            return
        m = ''
        for _ in range(10):
            m += str(random.choice(ctx.message.server.emojis)) + ' '
        await self.bot.say(m)

    # {prefix}kick
    @commands.command(pass_context=1, help="Fake kick someone")
    async def kick(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='kick', delete_message=False):
            return

        try:
            target = await self.bot.get_member_from_message(message=ctx.message, args=args, in_text=True)
        except ValueError:
            return

        if ctx.message.author == target:
            m = "You could just leave yourself if you want to go :thinking:"
            await self.bot.say(m)
            return

        await self.bot.on_member_message(target, "on_member_remove", 'left')

    # {prefix}kill <person>
    @commands.command(pass_context=1, help="Wish someone a happy death! (is a bit explicit)")
    async def kill(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='kill'):
            return

        try:
            target = await self.bot.get_member_from_message(message=ctx.message, args=args, in_text=True)
        except ValueError:
            return

        if ctx.message.author == target:
            await self.bot.say("Suicide is not the answer, 42 is")
            return

        await self.bot.say(random.choice(constants.kill).format(u=[" ".join(args)]))

    # {prefix}hug <person>
    @commands.command(pass_context=1, help="Give someone a little kiss!")
    async def kiss(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='kiss'):
            return
        try:
            target = await self.bot.get_member_from_message(message=ctx.message, args=args, in_text=True)
        except ValueError:
            return

        if ctx.message.author == target:
            await self.bot.say("{0} Trying to kiss yourself? Let me do that for you...\n*kisses {0}*".format(
                ctx.message.author.mention))
            return
        await self.bot.say(random.choice(constants.kisses).format(u=[ctx.message.author.mention, target.mention]))

    # {prefix}lenny <words>
    @commands.command(pass_context=1, help="( ͡° ͜ʖ ͡°)!")
    async def lenny(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='lenny'):
            return
        await self.bot.say(" ".join(args) + " ( ͡° ͜ʖ ͡°)")

    # {prefix}lottery <minutes> <description>
    @commands.command(pass_context=1, help="Set up a lottery!")
    async def lottery(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='lottery'):
            return
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
        mess = "Out of the " + str(len(lotterylist)) + " participants, " + random.sample(lotterylist, 1)[
            0].name + " is the lucky winner!"
        embed.add_field(name="Lottery winner", value=mess)
        await self.bot.say(embed=embed)

    # {prefix}pat <name>
    @commands.command(pass_context=1, help="PAT ALL THE THINGS!")
    async def pat(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='pat'):
            return

        try:
            errors = {'no_mention': ctx.message.author.mention + " You cant pat air lmao"}
            target = await self.bot.get_member_from_message(message=ctx.message, args=args, in_text=True, errors=errors)
        except ValueError:
            return

        if ctx.message.author == target:
            return await self.bot.say(ctx.message.author.mention + " One does not simply pat ones own head")

        time = datetime.datetime.utcnow()
        t = self.patTimes.get(ctx.message.author.id)

        if t and (time - t).total_seconds() < 60:
            await self.bot.say(ctx.message.author.mention + " Not so fast, b-b-baka!")
            return
        self.patTimes[ctx.message.author.id] = time

        n = dbcon.increment_pats(ctx.message.author.id, target.id)
        s = '' if n == 1 else 's'
        m = "{} has pat {} {} time{} now".format(ctx.message.author.mention, target.mention, n, s)
        if n % 100 == 0:
            m += "\nWoooooaaaaahh LEGENDARY!!!"
        elif n % 25 == 0:
            m += "\nWow, that is going somewhere!"
        elif n % 10 == 0:
            m += "\nSugoi!"
        await self.bot.say(m)

    # {prefix}hug <person>
    @commands.command(pass_context=1, help="Purr like you never purred before!")
    async def purr(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='purr'):
            return
        await self.bot.say(random.choice(constants.purr).format(ctx.message.author.mention))

    # {prefix}role <name>
    @commands.command(pass_context=1, help="Add or remove roles!")
    async def role(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='role'):
            return
        if len(args) <= 0:
            await self.bot.say("Usage: {}role <rolename without spaces> [\{user\}]".format(prefix))
            return
        else:
            rolename = args[0].lower()
        authorhasperms = ctx.message.channel.permissions_for(ctx.message.author).manage_roles or (
                ctx.message.server.owner.id == ctx.message.author.id)

        try:
            errors = {'no_mention': ctx.message.author.mention + " You cant pat air lmao"}
            user = await self.bot.get_member_from_message(message=ctx.message, args=args, errors=errors)
            if user != ctx.message.author and not authorhasperms:
                await self.bot.say("You do not have the permissions to give other people roles")
                return
        except ValueError:
            user = ctx.message.author

        if not (authorhasperms or rolename in ['nsfw', 'muted']):
            await self.bot.say("You lack the permissions for that")
            return

        role = None
        for r in ctx.message.server.roles:
            if r.name.lower().replace(' ', '') == rolename:
                role = r
                break
        if not role:
            await self.bot.say("Role {} not found".format(role))
            return

        try:
            if role in user.roles:
                await self.bot.remove_roles(user, role)
                await self.bot.say("Role {} succesfully removed".format(role.name))
                return
            else:
                await self.bot.add_roles(user, role)
                await self.bot.say("Role {} succesfully added".format(role.name))
                return
        except discord.Forbidden:
            await self.bot.say("I dont have the perms for that sadly...")

    # {prefix}serverinfo
    @commands.command(pass_context=1, help="Get the server's information!")
    async def serverinfo(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='serverinfo', cannot_be_private=True):
            return
        server = None
        if (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]) and len(args) > 0:
            for s in self.bot.servers:
                if s.name.lower().encode("ascii", "replace").decode("ascii") == ' '.join(args):
                    server = s
                    break
        if not server:
            server = ctx.message.server
        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=server.name, icon_url=ctx.message.author.avatar_url)
        if server.icon:
            embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Server ID", value=server.id)
        embed.add_field(name="Creation date", value=server.created_at)
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Members", value=server.member_count)
        embed.add_field(name="Owner", value='{} ({})'.format(server.owner.display_name, server.owner))
        embed.add_field(name="Custom Emoji", value=str(len(server.emojis)))
        embed.add_field(name="Roles", value=str(len(server.roles)))
        embed.add_field(name="Channels", value=str(len(server.channels)))
        if ctx.message.author.id in [constants.NYAid, constants.KAPPAid]:
            for c in server.channels:
                print(self.bot.prep_str_for_print(c.name))
        if len(server.features) > 0:
            f = ""
            for feat in server.features:
                f += "{}\n".format(feat)
            embed.add_field(name="Features", value=f)
        if server.splash:
            embed.add_field(name="Splash", value=server.splash)
        await self.bot.say(embed=embed)

    # {prefix}urban <query>
    @commands.command(pass_context=1, help="Search the totally official wiki!", aliases=["ud", "urbandictionary"])
    async def urban(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='urban'):
            return
        q = " ".join(args)
        if not q:
            await self.bot.say("...")
            return
        embed = discord.Embed(colour=0x0000FF)
        try:
            params = {'term': q}
            r = requests.get('http://api.urbandictionary.com/v0/define', params=params).json().get('list')
            if len(r) <= 0:
                embed.add_field(name="Definition", value="ERROR ERROR ... CANT HANDLE AWESOMENESS LEVEL")
                await self.bot.say(embed=embed)
            r = r[0]
            embed.add_field(name="Urban Dictionary Query", value=r.get('word'))
            definition = r.get('definition')
            if len(definition) > 500:
                definition = definition[:500] + '...'
            embed.add_field(name="Definition", value=definition, inline=False)
            example = r.get('example')
            if len(definition) < 500:
                if len(example) + len(definition) > 500:
                    example = example[:500 - len(definition)]
                if len(example) > 20:
                    embed.add_field(name="Example", value=example)
            embed.add_field(name="👍", value=r.get('thumbs_up'))
            embed.add_field(name="👎", value=r.get('thumbs_down'))
            await self.bot.say(embed=embed)
            return
        except KeyError:
            embed.add_field(name="Definition", value="ERROR ERROR ... CANT HANDLE AWESOMENESS LEVEL")
            await self.bot.say(embed=embed)

    # {prefix}userinfo <user>
    @commands.command(pass_context=1, help="Get a user's information!", aliases=["user", "info"])
    async def userinfo(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='userinfo'):
            return

        user = await self.bot.get_member_from_message(ctx.message, args, in_text=True)

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
        for r in range(1, len(user.roles)):
            m += "\n" + user.roles[r].name
        embed.add_field(name="Roles", value=m)
        await self.bot.say(embed=embed)

    # {prefix}wikipedia <query>
    @commands.command(pass_context=1, help="Search the wiki!", aliases=["wiki"])
    async def wikipedia(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='wikipedia'):
            return
        q = " ".join(args)
        if q == "":
            await self.bot.say("...")
            return
        embed = discord.Embed(colour=0x00FF00)
        try:
            s = wikipedia.summary(q, sentences=2)
            embed.add_field(name="Query: " + q, value=s)
            await self.bot.say(embed=embed)
            return
        except Exception as e:
            embed.add_field(name="Query: " + q, value="There are too much answers to give you the correct one...")
            await self.bot.say(embed=embed)
            return
