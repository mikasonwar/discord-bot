import discord
from discord.ext import commands
import libs.permissions as Permissions
import settings
import libs.database as database
import settings
import re

DB = database.getDB()
permissions = settings.permissions

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="birthdayreminders")
    @commands.check_any(permissions.isMaintainer())
    async def birthdayreminders(self, ctx):
        if ctx.invoked_subcommand is None:
            names = [f"`{c.name}`" for c in self.birthdayreminders.commands]
            await ctx.send(f'<:AYAYA:763899798365143060> Commands: [{" ".join(names)}] <:AYAYA:763899798365143060>')
    

    @birthdayreminders.command(name='list')
    @commands.check_any(permissions.isMaintainer())
    async def _list(self, ctx, page:int = 1):
        page_size = 10
        page = page - 1
        birthdayList = []

        #embed
        embedVar = discord.Embed(title="Lista de aniversários:", description=f"Página {page+1}", color=0x00ff00)
        embedVar.set_footer(text="Made by Mikas™")

        all_birthdays = DB(DB.birthdays).select()

        for row in all_birthdays[page*page_size:(page+1)*page_size]:
            birthdayList.append(f"    `{ctx.bot.get_user(int(row.user_id))}` - `{row.birthday}`")
            
        if birthdayList:
            embedVar.add_field(name="Aniversários", value='\n'.join(birthdayList), inline=False)
        else:
            embedVar.add_field(name="Aniversários", value='Não existe nenhuma nesta página!', inline=False)

        if len(all_birthdays[(page+1)*page_size:(page+2)*page_size]):
            embedVar.add_field(name="Próxima Página", value=f'\nFaz `{settings.prefix}birthdayreminders list {page+2}` para veres a próxima página!', inline=False)

        await ctx.send(embed=embedVar)      
        return
    
    @birthdayreminders.command(name='add')
    @commands.check_any(permissions.isMaintainer())
    async def add(self, ctx, member:discord.Member = None, date = ""):
        # Validações
        if member is None:
            await ctx.send("Tens de mencionar um user para poder adicionar o aniversário")
            return
        birthday = re.search('(\d{2}/\d{2})', date, re.IGNORECASE)
        if birthday is None:
            await ctx.send("Tens de mandar uma data com o seguinte formato: dd/mm")
            return
        
        # Inserir aniversário
        DB.birthdays.insert(user_id = member.id, birthday = birthday.group(1))
        DB.commit()
        await ctx.send("Aniversário inserido com sucesso!")
        return

    @birthdayreminders.command(name='delete')
    @commands.check_any(permissions.isMaintainer())
    async def delete(self, ctx, member:discord.Member = None):
        # Validações
        if member is None:
            await ctx.send("Tens de mencionar um user para poder remover o aniversário")
            return
        
        # Apagar aniversário
        DB(DB.birthdays.user_id == member.id).delete()
        DB.commit()
        await ctx.send("Aniversário apagado com sucesso!")
        return