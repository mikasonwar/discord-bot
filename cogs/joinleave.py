import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import libs.database as database
import settings

DB = database.getDB()
permissions = settings.permissions

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id != settings.mikas_guild or settings.production == False:
            return

        role = member.guild.get_role(settings.mikas_join_role)
        await member.add_roles(role)
        channel = self.bot.get_channel(int(settings.mikas_entry_leave))
        await channel.send(f"<@{member.id}>, bem vindo.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != settings.mikas_guild or settings.production == False:
            return

        bans = await member.guild.bans()
        banned = False
        for ban in bans:
            if ban.user.id == member.id:
                banned = True
                break

        channel = self.bot.get_channel(int(settings.mikas_entry_leave))
        if banned:
            await channel.send(f"o {member}, foi banido do discord.")
        else:
            await channel.send(f"o {member}, saiu do discord.")
