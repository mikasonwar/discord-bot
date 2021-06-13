import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
from discordTogether import DiscordTogether

permissions = settings.permissions

class Together(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_together = DiscordTogether(bot)

    async def create_link(self, ctx, widget):
        link = await self.discord_together.create_link(ctx.author.voice.channel.id, widget)
        message = f"Foi criado um discord-together do tipo `{widget}`:\n<{link}>"
        return await ctx.send(message)

    @commands.group(name="together")
    async def together(self, ctx):
        if ctx.invoked_subcommand is None:
            names = [f"`{c.name}`" for c in self.together.commands]
            await ctx.send(f'<:AYAYA:763899798365143060> Commands: [{" ".join(names)}] <:AYAYA:763899798365143060>')

    @together.command(name='youtube')
    async def youtube(self, ctx):
        return await self.create_link(ctx, "youtube")

    @together.command(name='poker')
    async def poker(self, ctx):
        return await self.create_link(ctx, "poker")

    @together.command(name='chess')
    async def chess(self, ctx):
        return await self.create_link(ctx, "chess")

    @together.command(name='amongus')
    async def betrayal(self, ctx):
        return await self.create_link(ctx, "betrayal")

    @together.command(name='fishing')
    async def fishing(self, ctx):
        return await self.create_link(ctx, "fishing")

    @together.command(name='custom')
    async def custom(self, ctx, id):
        return await self.create_link(ctx, id)