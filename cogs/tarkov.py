import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import random

permissions = settings.permissions

class Tarkov(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tarkytime', help='Random map de tarkov')
    async def tarky(self, ctx):
        maps = ["Interchange","Customs","Factory","Woods","Reserve","Shoreline"]
        if random.randint(0, 1) == 1:
            maps.append("Labs")
        await ctx.send(f'Calhou o mapa: {random.choice(maps)}')