import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import libs.database as database
import libs.presences as presences
import settings

DB = database.getDB()
permissions = settings.permissions

class Presences(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="presence")
    @commands.check_any(permissions.isMaintainer())
    async def presence(self, ctx):
        if ctx.invoked_subcommand is None:
            names = [f"`{c.name}`" for c in self.presence.commands]
            await ctx.send(f'<:AYAYA:763899798365143060> Commands: [{" ".join(names)}] <:AYAYA:763899798365143060>')

    @presence.command(name='list')
    @commands.check_any(permissions.isAdmin())
    async def _list(self, ctx, page:int=1):
        page_size = 10
        page=page-1
        presenceList = []

        embedVar = discord.Embed(title="Lista de presences:", description=f"Página {page+1}", color=0x00ff00)
        embedVar.set_footer(text="Made by Mikas™ & Marcel™")

        all_presences = DB(DB.presence).select()

        for row in all_presences[page*page_size:(page+1)*page_size]:
            presenceList.append(f"    `{row.id}` - `{row.value}`")
        
        if presenceList:
            embedVar.add_field(name="Presences", value='\n'.join(presenceList), inline=False)
        else:
            embedVar.add_field(name="Presences", value='Não existe nenhuma nesta página!', inline=False)

        if len(all_presences[(page+1)*page_size:(page+2)*page_size]):
            embedVar.add_field(name="Próxima Página", value=f'\nFaz `{settings.prefix}presence list {page+2}` para veres a próxima página!', inline=False)

        await ctx.send(embed=embedVar)
    
    @presence.command(name='add')
    @commands.check_any(permissions.isAdmin())
    async def add(self, ctx, *args):
        presences.addPresence(" ".join(args))
        await ctx.send("Presence adicionada")

    @presence.command(name='delete')
    @commands.check_any(permissions.isAdmin())
    async def delete(self, ctx, id:int):
        presences.deletePresence(id)
        await ctx.send("Presence apagada")


    # @commands.command(name='presence', help='Comando para gerir presences')
    # @commands.check_any(permissions.isAdmin())
    # async def mensagemPresences(self, ctx, arg1, *args):
    #     msg=""

    #     if arg1 == "list":
    #         page_size = 10
    #         if args is None or len(args) == 0 or args[0] is None:
    #             page=0
    #         else:
    #             page = int(args[0])-1
    #         presenceList = []


    #         embedVar = discord.Embed(title="Lista de presences:", description=f"Página {page+1}", color=0x00ff00)
    #         embedVar.set_footer(text="Made by Mikas™ & Marcel™")

    #         all_presences = DB(DB.presence).select()

    #         for row in all_presences[page*page_size:(page+1)*page_size]:
    #             presenceList.append(f"    `{row.id}` - `{row.value}`")
            
    #         if presenceList:
    #             embedVar.add_field(name="Presences", value='\n'.join(presenceList), inline=False)
    #         else:
    #             embedVar.add_field(name="Presences", value='Não existe nenhuma nesta página!', inline=False)

    #         if len(all_presences[(page+1)*page_size:(page+2)*page_size]):
    #             embedVar.add_field(name="Próxima Página", value=f'\nFaz `{settings.prefix}presence list {page+2}` para veres a próxima página!', inline=False)

    #         await ctx.send(embed=embedVar)      
    #         return        

    #     if arg1 == "add":
    #         presences.addPresence(' '.join(args))
    #         msg = "Presence adicionada"
    #     if arg1 == "delete":
    #         presences.deletePresence(int(args[0]))
    #         msg = "Presence apagada"
        
    #     await ctx.send(msg)   