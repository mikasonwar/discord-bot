import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import libs.database as database
import settings
import libs.user_roles as user_roles

DB = database.getDB()
permissions = settings.permissions

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='kick', help='Dá kick a um utilizador')
    @commands.check_any(permissions.isAdmin())
    async def kick(self, ctx, member:discord.Member = None):
        if member is None:
            await ctx.send("Só falta dizer qual é o utilizador para levar kick")
            return

        roles = [f"{c.id}" for c in member.roles]
        user_roles.remember_user_roles(member.id, ";".join(roles))

        try:
            await member.kick()
            await ctx.send(f"<:AYAYA:763899798365143060> <@{member.id}> foi kickado <:AYAYA:763899798365143060>") 
        except:
            await ctx.send(f"Dá-me um mais fácil...")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id != settings.mikas_guild or settings.production == False:
            return

        # Colocar roles antigas (caso tenha)
        roles_id = user_roles.get_user_roles(member.id)
        if roles_id is not None:
            roles = []
            for role_id in roles_id:
                role_id = int(role_id)
                role = member.guild.get_role(role_id)
                if role is not None and role.name != "@everyone" and role.id != settings.mikas_join_role:
                    roles.append(role)
            await member.add_roles(*roles)
            user_roles.delete_user_roles(member.id)

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
