import asyncio, discord, requests, os.path
from discord.ext import commands
from discord.ext.commands import Bot
from PIL import Image
from io import BytesIO
from os import listdir
from PIL.GifImagePlugin import getheader, getdata

# Normal commands
class Images:
    def __init__(self, my_bot):
        self.bot = my_bot

    @commands.command(pass_context=1, help="Show a profile pic, in max 200x200")
    async def pp(self, ctx, *args):
        self.bot.delete_message(ctx.message)
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        name = "temp/" + user.id + ".png"
        self.save_img(user.avatar_url, name)
        return await self.bot.send_file(ctx.message.channel, name)

    @commands.command(pass_context=1, help="You spin your head right round, right round. Like a record baby!")
    async def spin(self, ctx, *args):
        self.bot.delete_message(ctx.message)
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        name = "temp/" + user.id + ".png"
        self.save_img(user.avatar_url, name)
        
        l = []
        image = Image.open("./" + name)
        c = (image.width/6, image.height/6, 5*(image.width/6), 5*(image.height/6))
        l.append(image.crop(c))
        for i in range(37):
            l.append(image.rotate(i*10).crop(c))
        name = "temp/" + user.id + ".gif"
        l[0].save(name, save_all=1, append_images=l[1:37], loop=10, duration=1)
        await self.bot.send_file(ctx.message.channel, name)

    def save_img(self, url, name):
        if not os.path.isfile(name):
            # Download, resize and save file
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if img.height > 200:
                f = 200/img.height
                img = img.resize(((int)(img.height*f),(int)(img.width*f)))
            img.save(name)