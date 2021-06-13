import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings

permissions = settings.permissions

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cogtest', help='Cog Test!')
    async def cogtest(self, ctx):
        await ctx.send("teste!")