import asyncio, discord, requests, os.path
from discord.ext import commands
from discord.ext.commands import Bot
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from os import listdir
from PIL.GifImagePlugin import getheader, getdata

# Normal commands
class Images:
    def __init__(self, my_bot):
        self.bot = my_bot

    # {prefix}pp <user>
    @commands.command(pass_context=1, help="Show a profile pic, in max 200x200")
    async def pp(self, ctx, *args):
        await self.bot.delete_message(ctx.message)
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        return await self.bot.send_file(ctx.message.channel, str(user.avatar_url))
    
    # {prefix}meme <meme> <toptext>|<bottomtext>
    @commands.command(pass_context=1, help="Make a meme out of the arguments")
    async def meme(self, ctx, *args):
        await self.bot.delete_message(ctx.message)
        if (len(args) >= 1) & (args[0] == "list"):
            return await self.bot.send_message(ctx.message.channel, "Memelist: onedoesnotsimply")
        if len(args) < 2:
            return await self.bot.send_message(ctx.message.channel, "Meme to dank to make (usage: >meme <meme> <top-text>|<bottom-text>)")
        
        # Get meme picture and standard text
        meme = args[0].lower()
        if meme in ["one"]:
            img = Image.open("memes/OneDoesNotSimply.jpg")
            toptext = "One does not simply"
        else:
            if meme in ["victory baby", "baby"]:
                img = Image.open("memes/VBaby.png")
                toptext = ""
            else:
                if meme in ["brian", "badluckbrian"]:
                    img = Image.open("memes/Brian.jpg")
                    toptext = ""
                else:
                    return await self.bot.send_message(ctx.message.channel, "Memelist: onedoesnotsimply")

        # Get custom text
        text = " ".join(args[1:len(args)])
        if "|" in text:
            bottomtext = text.split("|")[1]
            toptext = text.split("|")[0]
        else:
            bottomtext = text

        # Add text to image
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("impact.ttf", 35)
        #w, h = draw.textsize(bottomtext)
        #st = (int)( (img.width/2) - (1.4*w))
        #w, h = draw.textsize(bottomtext)
        #sb = (int)( (img.width/2) - (1.4*w))
        draw.text((10, 10),toptext,(255,255,255),font=font)
        draw.text((190, 190),bottomtext,(255,255,255),font=font)

        # Save and send image
        name = 'memes/sample-out.jpg'
        img.save(name)
        await self.bot.send_file(ctx.message.channel, name)

    # {prefix}spin <user>
    @commands.command(pass_context=1, help="You spin your head right round, right round. Like a record baby!")
    async def spin(self, ctx, *args):
        await self.bot.delete_message(ctx.message)
        if len(ctx.message.mentions) <= 0:
            user = ctx.message.author
        else:
            user = ctx.message.mentions[0]
        name = "temp/" + user.id + ".png"
        if not os.path.isfile(name):
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

    # Download, resize and save file
    def save_img(self, url, name):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        if img.height > 200:
            f = 200/img.height
            img = img.resize(((int)(img.height*f),(int)(img.width*f)))
        img.save(name)