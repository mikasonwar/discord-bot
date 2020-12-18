import discord
import database
import os
import utils_mikas
from discord.ext import commands
from dotenv import load_dotenv

VERSION = '0.0.1.1'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


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
        self.bot = commands.Bot(command_prefix='!')

bot = DiscordBot().bot
DB = database.getDB()

def getBot():
    return DiscordBot().bot

def getBindedChannel(ctx):
    rows = DB(DB.config.key == "bindedChannel" and DB.config.guild == ctx.guild.id).select()
    if(len(rows)>0):
        return bot.get_channel(int(rows[0].value))
    else:
        return None

@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@bot.check
async def globally_check_channel(ctx):
    channel = getBindedChannel(ctx)
    return channel is None or ctx.command == bindChannel or channel == ctx.channel

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "chad" in message.content.lower():
        file = discord.File(utils_mikas.getRandomFileFromPath('hasan'))
        await message.channel.send(file=file)
    else:
        await bot.process_commands(message)

@bot.command(name='teste', help='Mensagem de teste!')
async def mensagemTeste(ctx):
    await ctx.send('Não me acordes!')
    
@bot.command(name='versao', help='Versão atual do bot')
async def mensagemTeste(ctx):
    await ctx.send(f'Versão {VERSION}')

@bot.command(name='testeArgs', help='Mensagem de Teste de argumentos')
async def mensagemArgumentos(ctx, arg1, arg2):
    await ctx.send(f'Argumento 1 : {arg1} | Argumento 2 : {arg2}')

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

@bot.event
async def on_disconnect():
    print("Disconnecting...")
    # exit()

def start_bot():
    bot.run(token)