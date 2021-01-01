import discord
import database
import os
import utils_mikas
import presences
import logger
from discord.ext import commands, tasks
from dotenv import load_dotenv

VERSION = '0.4.3'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('DISCORD_PREFIX', '!')
logger = logger.Logger("logs")
maintainers = ['Kappabanana#1662','mikasonwar#1337']


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

async def MangaDexNotification(name,image_url, url):
    rows = DB(DB.config.key == "bindedChannel").select()
    for row in rows:
        channel_id = row.value
        channel = bot.get_channel(channel_id)
        embedVar = discord.Embed(title=name, description="New Chapter", url=url, color=0x00ff00)
        embedVar.set_footer(text="Made by Mikas™")
        embedVar.set_image(url=image_url)
        embedVar.set_thumbnail(url=image_url)
        await bot.get_channel(int(channel_id)).send(embed=embedVar)

async def setRandomPresence():
    presence = presences.getRandomPresence()
    await bot.change_presence(status = presence.status, activity = presence.activity, afk = presence.afk)

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

@bot.command(name='presence', help='Mensagem de Teste de argumentos')
async def mensagemPresences(ctx, arg1, *args):
    if(ctx.author in maintainers):
        if arg1 == "list":
            for row in DB(DB.presence).select():
                msg = msg + "    " + str(row.id) + " - " + row.value
                print(row)
                # adicionar a msg para enviar
        if arg1 == "add":
            DB.presence.insert(value=' '.join(args))
            DB.commit()
            msg = "Presence adicionada"
        if arg1 == "delete":
            DB(DB.presence.id == int(args[0])).delete()
            DB.commit()
            msg = "Presence apagada"
        await ctx.send(msg)         
    else:
        await ctx.send("Não tens permissão para isto!") 

@bot.command(name='quit')
async def botquit(ctx):
    await ctx.send('Já vou dormir, nem queria!')
    await bot.logout()

@bot.command(name='bindChannel')
async def bindChannel(ctx):
    DB.config.update_or_insert(DB.config.key == 'bindedChannel' and DB.config.guild == ctx.guild.id,
                           key='bindedChannel',
                           guild=ctx.guild.id,
                           value=ctx.channel.id)
    DB.commit()                          
    await ctx.send('Agora só respondo neste channel! Haters!')
