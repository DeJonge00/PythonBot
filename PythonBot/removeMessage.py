import discord
from discord.ext import commands
import datetime


async def delete_message(bot, ctx, istyping=True):
    try:
        if not ctx.message.channel.is_private:
            await bot.delete_message(ctx.message)
    except discord.Forbidden:
        print("{} | {} | {} | member {}, no perms to delete message: {}".format(
            datetime.datetime.utcnow().strftime("%H:%M:%S"), ctx.message.server.name, ctx.message.channel.name,
            ctx.message.author.name.encode("ascii", "replace").decode("ascii"),
            ctx.message.content.encode("ascii", "replace").decode("ascii")))
    except discord.ext.commands.errors.CommandInvokeError:
        pass
    if istyping:
        await bot.send_typing(ctx.message.channel)
