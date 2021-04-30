import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import libs.guild_preset as guild_preset
import libs.database as database

DB = database.getDB()
permissions = settings.permissions

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='teste', help='Mensagem de teste!')
    async def mensagemTeste(self, ctx):
        await ctx.send('Não me acordes!')
    
    @commands.command(name='versao', help='Versão atual do bot')
    async def mensagemTeste(self, ctx):
        await ctx.send(f'Versão {settings.VERSION}')

    @commands.command(name='testeArgs', help='Mensagem de Teste de argumentos')
    async def mensagemArgumentos(self, ctx, arg1, arg2):
        await ctx.send(f'Argumento 1 : {arg1} | Argumento 2 : {arg2}')

    @commands.command(name='noobs', help='Permite ou não users com a role de usar comandos')
    @commands.check_any(permissions.isMaintainer())
    async def noobs(self, ctx):
        permissions.setAllowPermissions(not permissions.allow_permissions)
        await ctx.send(f"Alterado para `{permissions.allow_permissions}`") 

    @commands.command(name='switch', help='Trocar entre presets')
    @commands.check_any(permissions.isAdmin())
    async def switchGuildPreset(self, ctx, arg1):
        preset = guild_preset.getGuildPreset(arg1)
        if preset is None:
            await ctx.send(f"Não existe um preset com o nome `{arg1}`")
            return
        await ctx.guild.edit(name=preset.name,icon=preset.image)
        await ctx.send(f"Alterado para o preset `{preset.name}`")

    @commands.command(name='quit', help='Fazer com que o bot pare')
    @commands.check_any(permissions.isAdmin())
    async def botquit(self, ctx):
        await ctx.send('Já vou dormir, nem queria!')
        await ctx.bot.logout()

    @commands.command(name='bindChannel', help='Fazer bind a um channel')
    @commands.check_any(permissions.isAdmin())
    async def bindChannel(self, ctx):
        DB.config.update_or_insert(DB.config.key == 'bindedChannel' and DB.config.guild == ctx.guild.id,
                            key='bindedChannel',
                            guild=ctx.guild.id,
                            value=ctx.channel.id)
        DB.commit()                          
        await ctx.send('Agora só respondo neste channel! Haters!')