import discord
import database
import os
import utils_mikas
import presences
import logger
import guild_preset
from discord.ext import commands, tasks
from dotenv import load_dotenv

VERSION = '0.7.0'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('DISCORD_PREFIX', '!')
logger = logger.Logger("logs")
maintainers = os.getenv('MAINTANERS','151004374053814273,123928976589717510').split(',')
bot_user_role = os.getenv('BOT_USER_ROLE',797498453092859914)
bot_admin_role = os.getenv('BOT_ADMIN_ROLE',797498732035309580)
allow_permissions = os.getenv('ALLOW_PERMISSIONS',False) # Allow users with the roles to use commands (Maybe changing this to save in the DB)


# Singleton definition
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
       if cls not in instances:
            instances[cls] = cls(*args, **kw)
       return instances[cls]
    return _singleton


@singleton
class DiscordBot(object):
    def __init__(self):
        self.bot = commands.Bot(command_prefix=prefix)

# Fetch bot (singleton) and db

bot = DiscordBot().bot
DB = database.getDB()

# Helper Functions

def isUserMaintainer(id):
    return str(id) in maintainers

def getBot():
    return DiscordBot().bot

def start_bot():
    bot.run(token)

def getBindedChannel(ctx):
    rows = DB(DB.config.key == "bindedChannel" and DB.config.guild == ctx.guild.id).select()
    if(len(rows)>0):
        return bot.get_channel(int(rows[0].value))
    else:
        return None

async def sendNoPermissionMessage(ctx):
    await ctx.send("You do not have permission to run this command.") 

async def setRandomPresence():
    presence = presences.getRandomPresence()
    await bot.change_presence(status = presence.status, activity = presence.activity, afk = presence.afk)

def checkPermission(*roles):
    def predicate(ctx):
        return (isUserMaintainer(ctx.message.author.id) or (allow_permissions and commands.has_any_role(roles)))
    return commands.check(predicate)    

# Tasks 

@tasks.loop(seconds=10)
async def change_status():
    await setRandomPresence()

# Checks
@bot.check
async def globally_check_channel(ctx):
    channel = getBindedChannel(ctx)
    return channel is None or ctx.command == bindChannel or channel == ctx.channel

# Check apenas para fazer log
@bot.check
async def log_command(ctx):
    logger.warning(f"{ctx.author} used command {ctx.command}")
    return True

# Events

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    presences.setDefaultPresences()
    change_status.start()

@bot.event
async def on_message(message):
    # Bloquear o bot de responder a ele mesmo
    if message.author == bot.user:
        return

    # Bloquear DMs 
    if isinstance(message.channel,discord.DMChannel):
        logger.warning(f"{message.author} has tried to send a DM")
        return


    if "chad" in message.content.lower():
        logger.warning(f"{message.author} fired hasan event")
        file = discord.File(utils_mikas.getRandomFileFromPath('hasan'))
        await message.channel.send(file=file)
    else:
        await bot.process_commands(message)

@bot.event
async def on_disconnect():
    logger.info('Disconnecting...')
    # exit()

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(f'{error}') # Map each error for custom message?

# Commands

@bot.command(name='teste', help='Mensagem de teste!')
async def mensagemTeste(ctx):
    await ctx.send('Não me acordes!')
    
@bot.command(name='versao', help='Versão atual do bot')
async def mensagemTeste(ctx):
    await ctx.send(f'Versão {VERSION}')

@bot.command(name='testeArgs', help='Mensagem de Teste de argumentos')
async def mensagemArgumentos(ctx, arg1, arg2):
    await ctx.send(f'Argumento 1 : {arg1} | Argumento 2 : {arg2}')

@bot.command(name='noobs', help='Permite ou não users com a role de usar comandos')
async def noobs(ctx):
    if not isUserMaintainer(ctx.author.id):
        await sendNoPermissionMessage(ctx) 
        return
    global allow_permissions
    allow_permissions = not allow_permissions
    await ctx.send(f"Alterado para `{allow_permissions}`") 

@bot.command(name='switch', help='Trocar entre presets')
@commands.check_any(checkPermission(bot_admin_role))
async def switchGuildPreset(ctx, arg1):
    
    preset = guild_preset.getGuildPreset(arg1)
    if preset is None:
        await ctx.send(f"Não existe um preset com o nome `{arg1}`")
        return
    
    await ctx.guild.edit(name=preset.name,icon=preset.image)
    await ctx.send(f"Alterado para o preset `{preset.name}`")
    

@bot.command(name='presence', help='Comando para gerir presences')
@commands.check_any(checkPermission(bot_admin_role))
async def mensagemPresences(ctx, arg1, *args):
    msg=""

    if arg1 == "list":
        page_size = 10
        if args is None or len(args) == 0 or args[0] is None:
            page=0
        else:
            page = int(args[0])-1
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
            embedVar.add_field(name="Próxima Página", value=f'\nFaz `{prefix}presence list {page+2}` para veres a próxima página!', inline=False)

        await ctx.send(embed=embedVar)      
        return        

    if arg1 == "add":
        presences.addPresence(' '.join(args))
        msg = "Presence adicionada"
    if arg1 == "delete":
        presences.deletePresence(int(args[0]))
        msg = "Presence apagada"
    
    await ctx.send(msg)         

@bot.command(name='quit', help='Fazer com que o bot pare')
@commands.check_any(checkPermission(bot_admin_role))
async def botquit(ctx):
    await ctx.send('Já vou dormir, nem queria!')
    await bot.logout()

@bot.command(name='bindChannel', help='Fazer bind a um channel')
@commands.check_any(checkPermission(bot_admin_role))
async def bindChannel(ctx):
    DB.config.update_or_insert(DB.config.key == 'bindedChannel' and DB.config.guild == ctx.guild.id,
                           key='bindedChannel',
                           guild=ctx.guild.id,
                           value=ctx.channel.id)
    DB.commit()                          
    await ctx.send('Agora só respondo neste channel! Haters!')
