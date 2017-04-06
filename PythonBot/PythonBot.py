import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import constants
import datetime
import init
import log
import message_handler
import random
import responses
import sys

# Basic configs
pi = 3.14159265358979323846264

my_bot = Bot(command_prefix=commands.when_mentioned_or(">"), pm_help=1)

@my_bot.event
async def on_ready():
    print('Started bot')
    print("User: " + my_bot.user.name)
    print("ID: " + my_bot.user.id)
    print("Started at: " + datetime.datetime.utcnow().strftime("%H:%M:%S") + "\n")
    if not hasattr(my_bot, 'uptime'):
        my_bot.uptime = datetime.datetime.utcnow()
    await my_bot.change_presence(game=discord.Game(name='with lolis <3'), status=discord.Status.do_not_disturb)

# Add commands
import basic_commands
my_bot.add_cog(basic_commands.Basics(my_bot))
import music
my_bot.add_cog(music.Music(my_bot))
import image_commands
my_bot.add_cog(image_commands.Images(my_bot))
import mod_commands
my_bot.add_cog(mod_commands.Mod(my_bot))

# Handle incoming messages
@my_bot.event
async def on_message(message):
    if (message.author.bot):
        return
    if message.content:
        await message_handler.new(my_bot, message)
    if len(message.attachments) > 0:
        await message_handler.new_pic(my_bot, message)
    # Commands in the message
    await my_bot.process_commands(message)

# Logging
@my_bot.event
async def on_error(event, *args, **kwargs):
    await log.error(event, args)
@my_bot.event
async def on_message_edit(before, after):
    await message_handler.edit(before)
@my_bot.event
async def on_message_delete(message):
    await message_handler.deleted(message)
@my_bot.event
async def on_member_join(member):
    print("Member " + member.name + " just joined " + member.server)
@my_bot.event
async def on_member_leave(member):
    print("Member " + member.name + " just left " + member.server)
@my_bot.event
async def on_channel_delete(channel):
    await log.error(" deleted channel: " + channel.name)
@my_bot.event
async def on_channel_create(channel):
    await log.error(" created channel: " + channel.name)
@my_bot.event
async def on_channel_update(before, after):
    m = "channel updated:"
    if before.id != after.id:
        m += " id from: " + before.id + " to: " + after.id
    if before.name != after.name:
        m += " name from: " + before.name + " to: " + after.name
    if before.position != after.position:
        m += " position from: " + before.position + " to: " + after.position
    if before._permission_overwrites != after._permission_overwrites:
        m += " _permission_overwrites changed"
    await log.error(m)
@my_bot.event
async def on_member_update(before, after):
    m = "member " + before.name + " updated: "
    if before.name != after.name:
        m += " name from: " + before.name + " to: " + after.name
    if before.nick != after.nick:
        m += " nick from: " + before.nick + " to: " + after.nick
    for r in before.roles:
        if not r in after.roles:
            m += " +role: " + r.name
    for r in after.roles:
        if not r in before.roles:
            m += " -role: " + r.name
    if before.avatar != after.avatar:
        m += " avatar changed"
    if not m == "member " + before.name + " updated: ":
        await log.error(m)
@my_bot.event
async def on_server_update(before, after):
    m = "server " + before.name + " updated: "
    if before.name != after.name:
        m += " name from: " + before.name + " to: " + after.name
    for r in before.roles:
        if not r in after.roles:
            m += " +role: " + r.name
    for r in after.roles:
        if not r in before.roles:
            m += " -role: " + r.name
    if before.region != after.region:
        m += " region from: " + before.region + " to: " + after.region
    if not m == "server " + before.name + " updated: ":
        await log.error(m)
@my_bot.event
async def on_server_role_update(before, after):
    m = "role " + before.name + " updated: "
    if before.name != after.name:
        m += " name from: " + before.name + " to: " + after.name
    for r in before.permissions:
        if not r in after.permissions:
            m += " +permission: " + r.name
    for r in after.permissions:
        if not r in before.permissions:
            m += " -permission: " + r.name
    if not m == "role " + before.name + " updated: ":
        await log.error(m)
@my_bot.event
async def on_server_emojis_update(before, after):
    m = "emojis " + before.name + " updated: "
    if len(before) != len(after):
        m += " size from: " + len(before) + " to: " + len(after)
    if not m == "emojis " + before.name + " updated: ":
        await log.error(m)
@my_bot.event
async def on_member_ban(member):
    await log.error("user " + member.name + " banned")
@my_bot.event
async def on_member_unban(member):
    await log.error("user " + member.name + " unbanned")

# Actually run the bot
my_bot.run(constants.bot_token)