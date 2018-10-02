import discord, constants, sqlite3, os, requests, dbconnect, re
from discord.ext import commands
from random import randint
from PIL import Image
from io import BytesIO
from datetime import datetime


# Mod commands
class Mod:
    def __init__(self, my_bot):
        self.bot = my_bot
        print('Mod started')

    # {prefix}banish <@person>
    @commands.command(pass_context=1, help="BANHAMMER")
    async def banish(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='banish'):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not ((ctx.message.author.id == constants.NYAid) or perms.kick_members or perms.administrator):
            await self.bot.say("Hahahaha, no")
            return
        for user in ctx.message.mentions:
            await self.bot.kick(user)

    # {prefix}invite <#members> <servername>
    @commands.command(pass_context=1, help="Create an invitation for this channel!")
    async def invite(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='invite'):
            return

        # Check permissions
        userperms = ctx.message.channel.permissions_for(ctx.message.author)
        userperms = userperms.create_instant_invite or userperms.administrator or userperms.manage_server
        if not userperms:
            await self.bot.say('You do not have the permissions for that...')
            return

        bb_member = ctx.message.server.get_member(self.bot.user.id)
        bb_perms = ctx.message.channel.permissions_for(bb_member).create_instant_invite
        if not bb_perms:
            await self.bot.say('I do not have the permissions for that...')
            return

        # Invite settings
        if len(args) > 0:
            try:
                user_limit = int(args[0])
            except ValueError:
                await self.bot.say('That is not a number, silly')
                return
        else:
            user_limit = 0

        if len(args) > 1 and ctx.message.author.id == constants.NYAid:
            servers = [s for s in self.bot.servers if
                       ''.join([x for x in s.name.lower() if x.isalpha()]).startswith(''.join(args[1:]))]
            if len(servers) <= 0:
                await self.bot.say('I dunno that one...')
                return
            dest = await self.bot.ask_one_from_multiple(ctx.message, servers, question='Which server did you mean?')
        else:
            dest = ctx.message.channel

        # Create and send invite
        try:
            inv = await self.bot.create_invite(dest, max_uses=user_limit, unique=False)
        except discord.HTTPException:
            await self.bot.say('Something went wrong when asking discord for an invite link')
            return
        await self.bot.say("Invite all the weebs!\n" + str(inv))

    # {prefix}newpp <attach new pp>
    @commands.command(pass_context=1, help="Give me a new look")
    async def newpp(self, ctx):
        if not (ctx.message.author.id in [constants.NYAid, constants.KAPPAid]):
            await self.bot.say("Hahahaha, no")
            return
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].get('url')
        elif len(ctx.message.mentions) > 0:
            url = '.'.join(ctx.message.mentions[0].avatar_url.split('.')[:-1]) + '.png'
            print(url)
        else:
            await self.bot.say('Pls give me smth...')
            return
        try:
            # TODO: Fix saving pic first
            name = 'temp/newpp.png'
            Image.open(BytesIO(requests.get(url).content)).save(name)
            if not await self.bot.pre_command(message=ctx.message, command='newpp'):
                return
            with open(name, 'rb') as file:
                await self.bot.edit_profile(avatar=file.read())
            await self.bot.say('Make-up is done sweety <3')
        except requests.exceptions.MissingSchema:
            await self.bot.say('Thats not a valid target')
        except OSError:
            await self.bot.say('Thats not a valid target')
        except discord.HTTPException:
            await self.bot.say('Discord pls')
        finally:
            try:
                os.remove(name)
            except:
                pass

    # {prefix}nickname <@person>
    @commands.command(pass_context=1, help="Nickname a person", aliases=["nick", "nn"])
    async def nickname(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='nickname', is_typing=False):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if len(ctx.message.mentions) > 0:
            if len(args) > 1:
                if not (ctx.message.author.id == constants.NYAid or perms.manage_nicknames or perms.administrator):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], " ".join(args[1:]))
            else:
                if not (ctx.message.author.id == constants.NYAid or perms.change_nickname or perms.administrator):
                    await self.bot.say("Hahahaha, no")
                    return
                await self.bot.change_nickname(ctx.message.mentions[0], "")

    # {prefix}purge <amount>
    @commands.command(pass_context=1, help="Remove a weird chat")
    async def purge(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='purge', is_typing=False):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_messages or perms.administrator):
            await self.bot.say("Hahahaha, no")
            return
        if len(args) > 0:
            try:
                l = int(args[0])
            except ValueError:
                l = 10
        else:
            l = 10
        if len(ctx.message.mentions) > 0:
            def c(message):
                return message.author in ctx.message.mentions

            return await self.bot.purge_from(ctx.message.channel, check=c, limit=l)
        await self.bot.purge_from(ctx.message.channel, limit=l)

    # {prefix}setgoodbye <message>
    @commands.command(pass_context=1, help="Sets a goodbye message")
    async def setgoodbye(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='setgoodbye'):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_server or perms.administrator):
            await self.bot.say("Hahahaha, no")
            return
        if len(" ".join(args)) > 120:
            await self.bot.say("Sorry, this message is too long...")
            return
        if re.match('.*{.+}.*', " ".join(args)):
            await self.bot.say("Something went terribly wrong...")
            return
        dbconnect.set_message('on_member_remove', ctx.message.server.id, ctx.message.channel.id, " ".join(args))
        if len(args) > 0:
            await self.bot.say("Goodbye message for this server is now: " + " ".join(args).format("<user mention>"))
            return
        await self.bot.say("Goodbye message for this server has been reset")

    # {prefix}setwelcome <message>
    @commands.command(pass_context=1, help="Sets a welcome message")
    async def setwelcome(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='setwelcome'):
            return
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if not (ctx.message.author.id == constants.NYAid or perms.manage_server or perms.administrator):
            await self.bot.say("Hahahaha, no")
            return
        if len(" ".join(args)) > 120:
            await self.bot.say("Sorry, this message is too long...")
            return
        if re.match('.*{.+}.*', " ".join(args)):
            await self.bot.say("Something went terribly wrong...")
            return
        dbconnect.set_message('on_member_join', ctx.message.server.id, ctx.message.channel.id, " ".join(args))
        if len(args) > 0:
            await self.bot.say("Welcome message for this server is now: " + " ".join(args).format("<user mention>"))
            return
        await self.bot.say("Welcome message for this server has been reset")

    # Test command
    @commands.command(pass_context=1, hidden=1, help="test")
    async def test(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='test', delete_message=False):
            return
        if not (ctx.message.author.id == constants.NYAid or ctx.message.author.id == constants.KAPPAid):
            await self.bot.say("Hahahaha, no")
            return
        print('test')
