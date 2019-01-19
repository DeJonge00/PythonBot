import math
import discord
from discord.ext.commands import Bot

EMBED_COLOR = 0x710075


class EmbedList:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.lists = {}

    async def make_list(self, items: [], title: str, channel: discord.Channel=None, message: discord.Message=None, page=0, items_per_page=10):
        embed = discord.Embed(colour=EMBED_COLOR)
        if page == -1:
            page = math.floor(len(items) / items_per_page)
        elif len(items) < (items_per_page * page):
            raise ValueError('Max page number is ' + str(math.ceil(len(items) / items_per_page)))
        top_end = (items_per_page * (page + 1))
        if top_end > len(items):
            top_end = len(items)
        top_start = (items_per_page * page)
        result = ""

        for i in range(top_start, top_end):
            rank = i + 1
            result += '{})  {}\n'.format(rank, items[i])
        embed.add_field(name="{}, page {}".format(title, page + 1), value=result)
        if message:
            message = await self.bot.edit_message(message, embed=embed)
        else:
            message = await self.bot.send_message(channel, embed=embed)
            await self.add_list_emoji(message)
        self.set_list_message(page, title, items, message)
        return message

    def set_list_message(self, page: int, title: str, items: str, message: discord.Message):
        self.lists[message.id] = (page, title, items)

    async def add_list_emoji(self, message):
        await self.bot.add_reaction(message, "⏮")
        await self.bot.add_reaction(message, '⬅')
        await self.bot.add_reaction(message, "➡")
        await self.bot.add_reaction(message, "⏭")
        await self.bot.add_reaction(message, "\N{BROKEN HEART}")

    async def handle_reaction(self, reaction: discord.Reaction):
        if reaction.message.id not in self.lists.keys():
            return
        for m in await self.bot.get_reaction_users(reaction):
            if m.id != self.bot.user.id:
                await self.bot.remove_reaction(reaction.message, reaction.emoji, m)

        page, title, items = self.lists.get(reaction.message.id)
        try:
            if reaction.emoji == "⏮":
                await self.make_list(items=items, title=title, page=0, message=reaction.message)
            if reaction.emoji == '⬅':
                await self.make_list(items=items, title=title, page=page-1, message=reaction.message)
            if reaction.emoji == '➡':
                await self.make_list(items=items, title=title, page=page+1, message=reaction.message)
            if reaction.emoji == "⏭":
                await self.make_list(items=items, title=title, page=-1, message=reaction.message)
        except ValueError:
            pass
