import discord
import libs.database as database
import libs.presences as presences
from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord.utils import get
from cogs.general import General
from cogs.presences import Presences
from cogs.birthdays import Birthdays
from cogs.joinleave import JoinLeave
import settings
import libs.messagehandler as MessageHandler

# Defenir o intent para apanhar member_joins
# https://discord.com/developers/applications/ Ligar o intent de membros caso esteja desligado
intents = discord.Intents.default()
intents.members = True

logger = settings.logger

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
        self.bot = commands.Bot(command_prefix=settings.prefix, intents=intents)

# Fetch bot (singleton) and db

bot = DiscordBot().bot
DB = database.getDB()

# Helper Functions

def getBot():
    return DiscordBot().bot

def start_bot():
    bot.add_cog(General(bot))
    bot.add_cog(Presences(bot))
    bot.add_cog(Birthdays(bot))
    bot.add_cog(JoinLeave(bot))
    bot.run(settings.token)

def getBindedChannel(ctx):
    rows = DB(DB.config.key == "bindedChannel" and DB.config.guild == ctx.guild.id).select()
    if(len(rows)>0):
        return bot.get_channel(int(rows[0].value))
    else:
        return None

async def sendNoPermissionMessage(ctx):
    await ctx.send("Não tens permissão para correr este comando.") 

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
    return channel is None or ctx.command.name == "bindChannel" or channel == ctx.channel

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

    await MessageHandler.handle(logger,message)
    
    await bot.process_commands(message)

@bot.event
async def on_disconnect():
    logger.info('Disconnecting...')
    # exit()

@bot.event
async def on_command_error(ctx, error):
    if(type(error).__name__ == "CheckAnyFailure"):
        logger.info(f'{ctx.message.author} tried to use a command that he doesn\'t have permission')
        await sendNoPermissionMessage(ctx)
    elif isinstance(error, commands.BadArgument):
        logger.info(f'{ctx.message.author} tried to use a command but got {error}')
        await ctx.send('Cá burro dréd, nem sabes usar o comando')
    else:
        await ctx.send('Já partiste o caralho do bot fds')
        logger.info(f'{ctx.message.author} {error}')

# Commands

# Passamos tudo para cogs :)