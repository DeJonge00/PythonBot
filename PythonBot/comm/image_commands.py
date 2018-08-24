from datetime import datetime
from io import BytesIO

import constants
import discord
import requests
import send_random
from PIL import Image
from discord.ext import commands

TIMER = True


# Normal commands
class Images:
    def __init__(self, my_bot):
        self.bot = my_bot
        self.image_timers = {}

    # {prefix}pp <user>
    @commands.command(pass_context=1, aliases=['avatar', 'picture'], help="Show a profile pic, in max 200x200")
    async def pp(self, ctx):
        if not await self.bot.pre_command(message=ctx.message, command='pp'):
            return
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        embed = discord.Embed(colour=0x000000)
        embed.set_author(name=str(user.name))
        embed.set_image(url=user.avatar_url)
        return await self.bot.send_message(ctx.message.channel, embed=embed)

    async def send_picture_template_command(self, message: discord.Message, channel: discord.Channel, command: str,
                                            pic_links: list = None, pic_folder: str = None):
        if not await self.bot.pre_command(message=message, command=command):
            return
        if TIMER:
            if not self.image_timers.get(command):
                self.image_timers[command] = {}
            if (datetime.utcnow() - self.image_timers.get(command).get(channel.id,
                                                                       datetime.fromtimestamp(0))).seconds < 60:
                return
            await self.bot.send_typing(channel)
            self.image_timers[command][channel.id] = datetime.utcnow()
        if pic_links:
            await send_random.embedded_pic(self.bot, channel, command, self.bot.user.avatar_url, pic_links)
        elif pic_folder:
            await send_random.file(self.bot, channel, pic_folder)

    # {prefix}60
    @commands.command(pass_context=1, help="Help get cancer out of this world!", aliases=["60"])
    async def fps(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'fps', pic_folder='60')

    # {prefix}biribiri
    @commands.command(pass_context=1, help="Waifu == laifu!", aliases=["biri"])
    async def biribiri(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'biribiri', pic_folder='biribiri')

    # {prefix}cat
    @commands.command(pass_context=1, help="CATS!")
    async def cat(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'cat', pic_folder='cat')

    # {prefix}cuddle
    @commands.command(pass_context=1, help="Cuddles everywhere!")
    async def cuddle(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'cuddle', pic_folder='cuddle')

    # {prefix}ded
    @commands.command(pass_context=1, help="Ded chat reminder!")
    async def ded(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'ded', pic_folder='ded')

    # {prefix}heresy
    @commands.command(pass_context=1, help="Fight the heresy!")
    async def heresy(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'heresy', pic_folder='heresy')

    # {prefix}happy
    @commands.command(pass_context=1, help="Awwww yeaaahhh!")
    async def happy(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'happy', pic_links=constants.happy_gifs)

    # {prefix}lewd
    @commands.command(pass_context=1, help="LLEEEEEEEEWWDD!!!")
    async def lewd(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'lewd', pic_links=constants.lewd_gifs)

    # {prefix}nonazi
    @commands.command(pass_context=1, help="Try to persuade Lizzy with anti-nazi-propaganda!")
    async def nonazi(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'nonazi', pic_folder='nonazi')

    # {prefix}nyan
    @commands.command(pass_context=1, help="Nyanyanyanyanyanyanyanyanya!")
    async def nyan(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'nyan', pic_links=constants.nyan_gifs)

    # {prefix}otter
    @commands.command(pass_context=1, help="OTTERSSSSS!")
    async def otter(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'otter',
                                                 pic_links=constants.otters)

    # {prefix}plsno
    @commands.command(pass_context=1, help="Nonononononono!", aliases=['nopls'])
    async def plsno(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'plsno',
                                                 pic_links=constants.plsno_gifs)

    # {prefix}sadness
    @commands.command(pass_context=1, help="Cri!")
    async def sadness(self, ctx):
        await self.send_picture_template_command(ctx.message, ctx.message.channel, 'sadness',
                                                 pic_links=constants.sad_gifs)



    # Download, resize and save file
    def save_img(self, url, name):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        if img.height > 200:
            f = 200 / img.height
            img = img.resize((int(img.height * f), int(img.width * f)))
        img.save(name)
