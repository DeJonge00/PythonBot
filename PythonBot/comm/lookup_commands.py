import discord
import re
import requests
from discord.ext import commands

from secret.secrets import osu_api_key


# Normal commands
class Lookup:
    def __init__(self, my_bot):
        self.bot = my_bot
        print('Lookup started')

    async def lookup(self, query: str, search_url: str, search_for: str, min_results: int, skip_results: int, result_url):
        page = requests.get(search_url, {'q': query})
        if page.status_code != 200:
            await self.bot.say('Uh oh, I must have made a wrong requests')
            return
        n = re.findall(search_for + '[0-9]*/', page.text.replace(' ', '').replace('\n', ''))
        if len(n) <= min_results:
            await self.bot.say('No results found for that...')
            return
        await self.bot.say(result_url + re.findall('[0-9]+', n[skip_results])[0])

    async def am_lookup(self, query, genre):
        await self.lookup(query, 'https://myanimelist.net/search/all', 'myanimelist.net/' + genre + '/', 16, 0, 'https://myanimelist.net/' + genre + '/')

    # {prefix}anime <name>
    @commands.command(pass_context=1, help="Look up an anime!", aliases=['mal', 'myanimelist'])
    async def anime(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='anime'):
            return
        await self.am_lookup(' '.join(args), 'anime')

    # {prefix}manga <name>
    @commands.command(pass_context=1, help="Look up a manga!")
    async def manga(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='manga'):
            return
        await self.am_lookup(' '.join(args), 'manga')

    # {prefix}movie <name>
    @commands.command(pass_context=1, help="Look up a movie!", aliases=['imdb'])
    async def movie(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='manga'):
            return
        await self.lookup(' '.join(args), 'https://www.imdb.com/find', '/title/tt', 2, 2, 'https://www.imdb.com/title/tt')

    # {prefix}osu <osu user>
    @commands.command(pass_context=1, help="Look up someones osu stats!")
    async def osu(self, ctx, *args):
        if not await self.bot.pre_command(message=ctx.message, command='osu'):
            return

        if len(args) <= 0:
            await self.bot.say('Please provide a username to look for')
            return
        user = ' '.join(args)

        url = 'https://osu.ppy.sh/api/get_user'
        params = {'k': osu_api_key,
                  'u': user,
                  'm': 0,
                  'type': 'string'}
        r = requests.get(url, params=params)
        if r.status_code != 200:
            await self.bot.say('Uh oh, the osu site did not give me any information for my request')
            return
        r = r.json()
        if len(r) <= 0:
            await self.bot.say('Ehhm, there is no user with that name...')
            return
        r = r[0]

        embed = discord.Embed(colour=0xFF0000)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url='https://a.ppy.sh/{}?.jpg'.format(r.get('user_id')))
        embed.add_field(name="Username", value=r.get('username'))
        embed.add_field(name='Profile link', value='https://osu.ppy.sh/u/{}'.format(r.get('user_id')))
        embed.add_field(name="Playcount", value=r.get('playcount'))
        embed.add_field(name="Total score", value=r.get('total_score'))
        embed.add_field(name="Ranked score", value=r.get('ranked_score'))
        embed.add_field(name="Global rank", value='#' + r.get('pp_rank'))
        embed.add_field(name="Country rank", value='#{} ({})'.format(r.get('pp_country_rank'), r.get('country')))
        embed.add_field(name="Accuracy", value='{}%'.format(round(float(r.get('accuracy')), 3)))
        embed.add_field(name="Hours played", value=str(int(int(r.get('total_seconds_played')) / 3600)))
        embed.add_field(name="Total maps with SS", value=r.get('count_rank_ss'))
        embed.add_field(name="Total maps with S", value=r.get('count_rank_s'))

        await self.bot.say(embed=embed)
