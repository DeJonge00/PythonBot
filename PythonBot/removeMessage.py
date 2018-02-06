import asyncio, discord, secret.constants as constants
from discord.ext import commands
from discord.ext.commands import Bot

async def deleteMessage(bot, ctx, istyping=True):
    try:
        await bot.delete_message(ctx.message)
    except discord.Forbidden:
        print(ctx.message.server.name + " | No permission to delete messages")
    except discord.ext.commands.errors.CommandInvokeError:
        pass
    if istyping:
        await bot.send_typing(ctx.message.channel);

async def nyaCheck(bot, ctx):
    if ctx.message.author.id != constants.NYAid:
        m = await bot.send_message(ctx.message.channel, "Hahaha, no.")
        await asyncio.sleep(10)
        try:
            await bot.delete_message(m)
        except discord.Forbidden:
            print(ctx.message.server.name + " | No permission to delete messages")
        except discord.ext.commands.errors.CommandInvokeError:
            pass
        return False
    return True