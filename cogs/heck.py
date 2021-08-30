import json
import os
import sys
import aiohttp
import discord
import asyncio
import math
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class allies(commands.Cog, name="allies"):
    def __init__(self, bot):
        self.bot = bot
        self.api_token = config['api_token']
        self.headers = {'Authorization': f"Token {self.api_token}"}
        self.base_url = config['base_url']
        self.url = f"{self.base_url}/allies/"

    @commands.command(name="allies")
    @commands.guild_only()
    async def allies(self, context, *, allyname):
        """
        Return a list of allies from given username.
        """
        buttons = ["◀️", "▶️"]
        async with aiohttp.ClientSession() as session:
            page = 1
            raw_response = await session.get(f"{self.url}?search={allyname}&page={page}", headers=self.headers)
            response = await raw_response.text()
            response = json.loads(response)
            if response.get('detail'):
                await context.send("Token Expired")
            else:
                allies = response['results']
                count = math.ceil(response['count'] / 20)
                embed = discord.Embed(title=f"__**{allyname} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                if not allies:
                    await context.send("No results.")
                else:
                    for ally in allies:
                        username = ally['username']
                        group_tag = ally['group_tag']
                        cost = ally['cost']
                        last_modified = ally['last_modified']
                        grass = ally['biome3_attack_multiplier'] / 100
                        badlands = ally['biome4_attack_multiplier'] / 100
                        swamp = ally['biome5_attack_multiplier'] / 100
                        total = round(grass + badlands + swamp, 2)
                        embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                    embed.set_footer(text=f'Page {page} of {count}')
                    message = await context.send(embed=embed)
                    for b in buttons:
                        await message.add_reaction(b)

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: r.message.id == message.id and u.id == context.author.id)
                            em = str(reaction.emoji)
                        except asyncio.TimeoutError:
                            await message.delete()
                            return
                        
                        if user!=self.bot.user:
                            await message.remove_reaction(emoji=em, member=user)

                        if em == '▶️':
                            page = page+1
                            raw_response = await session.get(f"{self.url}?search={allyname}&page={page}", headers=self.headers)
                            response = await raw_response.text()
                            response = json.loads(response)
                            try:
                                allies = response['results']
                                count = math.ceil(response['count'] / 20)
                                embed = discord.Embed(title=f"__**{allyname} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                for ally in allies:
                                    username = ally['username']
                                    group_tag = ally['group_tag']
                                    cost = ally['cost']
                                    last_modified = ally['last_modified']
                                    grass = ally['biome3_attack_multiplier'] / 100
                                    badlands = ally['biome4_attack_multiplier'] / 100
                                    swamp = ally['biome5_attack_multiplier'] / 100
                                    total = round(grass + badlands + swamp, 2)
                                    embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            except KeyError:
                                embed = discord.Embed(title=f"__**{allyname} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                embed.add_field(name=f'**{allyname}**', value=f'> No More Results',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            await message.edit(embed = embed)

                        if em == '◀️':
                            page = page-1
                            raw_response = await session.get(f"{self.url}?search={allyname}&page={page}", headers=self.headers)
                            response = await raw_response.text()
                            response = json.loads(response)
                            try:
                                allies = response['results']
                                count = math.ceil(response['count'] / 20)
                                embed = discord.Embed(title=f"__**{allyname} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                for ally in allies:
                                    username = ally['username']
                                    group_tag = ally['group_tag']
                                    cost = ally['cost']
                                    last_modified = ally['last_modified']
                                    grass = ally['biome3_attack_multiplier'] / 100
                                    badlands = ally['biome4_attack_multiplier'] / 100
                                    swamp = ally['biome5_attack_multiplier'] / 100
                                    total = round(grass + badlands + swamp, 2)
                                    embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            except KeyError:
                                embed = discord.Embed(title=f"__**{allyname} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                embed.add_field(name=f'**{allyname}**', value=f'> No More Results',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            await message.edit(embed = embed)


    @commands.command(name="price")
    @commands.guild_only()
    async def allies(self, context, *, price):
        """
        Return a list of allies from given price.
        """
        buttons = ["◀️", "▶️"]
        async with aiohttp.ClientSession() as session:
            page = 1
            raw_response = await session.get(f"{self.url}?cost={price}&page={page}", headers=self.headers)
            response = await raw_response.text()
            response = json.loads(response)
            if response.get('detail'):
                await context.send("Token Expired")
            else:
                allies = response['results']
                count = math.ceil(response['count'] / 20)
                embed = discord.Embed(title=f"__**{price} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                if not allies:
                    await context.send("No results.")
                else:
                    for ally in allies:
                        username = ally['username']
                        group_tag = ally['group_tag']
                        cost = ally['cost']
                        last_modified = ally['last_modified']
                        grass = ally['biome3_attack_multiplier'] / 100
                        badlands = ally['biome4_attack_multiplier'] / 100
                        swamp = ally['biome5_attack_multiplier'] / 100
                        total = round(grass + badlands + swamp, 2)
                        embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                    embed.set_footer(text=f'Page {page} of {count}')
                    message = await context.send(embed=embed)
                    for b in buttons:
                        await message.add_reaction(b)

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: r.message.id == message.id and u.id == context.author.id)
                            em = str(reaction.emoji)
                        except asyncio.TimeoutError:
                            await message.delete()
                            return
                        
                        if user!=self.bot.user:
                            await message.remove_reaction(emoji=em, member=user)

                        if em == '▶️':
                            page = page+1
                            raw_response = await session.get(f"{self.url}?search={price}&page={page}", headers=self.headers)
                            response = await raw_response.text()
                            response = json.loads(response)
                            try:
                                allies = response['results']
                                count = math.ceil(response['count'] / 20)
                                embed = discord.Embed(title=f"__**{price} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                for ally in allies:
                                    username = ally['username']
                                    group_tag = ally['group_tag']
                                    cost = ally['cost']
                                    last_modified = ally['last_modified']
                                    grass = ally['biome3_attack_multiplier'] / 100
                                    badlands = ally['biome4_attack_multiplier'] / 100
                                    swamp = ally['biome5_attack_multiplier'] / 100
                                    total = round(grass + badlands + swamp, 2)
                                    embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            except KeyError:
                                embed = discord.Embed(title=f"__**{price} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                embed.add_field(name=f'**{price}**', value=f'> No More Results',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            await message.edit(embed = embed)

                        if em == '◀️':
                            page = page-1
                            raw_response = await session.get(f"{self.url}?search={price}&page={page}", headers=self.headers)
                            response = await raw_response.text()
                            response = json.loads(response)
                            try:
                                allies = response['results']
                                count = math.ceil(response['count'] / 20)
                                embed = discord.Embed(title=f"__**{price} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                for ally in allies:
                                    username = ally['username']
                                    group_tag = ally['group_tag']
                                    cost = ally['cost']
                                    last_modified = ally['last_modified']
                                    grass = ally['biome3_attack_multiplier'] / 100
                                    badlands = ally['biome4_attack_multiplier'] / 100
                                    swamp = ally['biome5_attack_multiplier'] / 100
                                    total = round(grass + badlands + swamp, 2)
                                    embed.add_field(name=f'**{username}**', value=f'> Clan: {group_tag}\n> G: {grass}% B: {badlands}% S: {swamp}% Total: {total}%\n> Cost: {cost}\n> Last Updated: {last_modified}',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            except KeyError:
                                embed = discord.Embed(title=f"__**{price} Results:**__", color=0x03f8fc,timestamp= context.message.created_at)
                                embed.add_field(name=f'**{price}**', value=f'> No More Results',inline=False)
                                embed.set_footer(text=f'Page {page} of {count}')
                            await message.edit(embed = embed)
def setup(bot):
    bot.add_cog(allies(bot))