import asyncio, discord, secret.constants as constants
from discord.ext import commands
from discord.ext.commands import Bot

async def deleteMessage(bot, ctx, istyping=True):
    try:
        await bot.delete_message(ctx.message)
    except discord.Forbidden:
        print(ctx.message.server + " | No permission to delete messages")
    if istyping:
        await bot.send_typing(ctx.message.channel);

async def nyaCheck(bot, ctx):
    if ctx.message.author.id != constants.NYAid:
        m = await bot.send_message(ctx.message.channel, "Hahaha, no.")
        asyncio.sleep(30)
        try:
            await bot.delete_message(m)
        except discord.Forbidden:
            print(ctx.message.server + " | No permission to delete messages")
        return False
    return True