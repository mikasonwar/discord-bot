import discord
import libs.utils_mikas as utils_mikas

async def handle(logger,message):
    if await checkChad(logger,message):
        return True
    if await checkBafalas(logger, message):
        return True
    return False

async def checkChad(logger,message):
    if "chad" in message.content.lower().split(" "):
        logger.warning(f"{message.author} fired hasan event")
        file = discord.File(utils_mikas.getRandomFileFromPath('hasan'))
        await message.channel.send(file=file)
        return True
    return False

async def checkBafalas(logger,message):
    if "bafalas" in message.content.lower().split(" "):
        logger.warning(f"{message.author} fired bafalas event")
        await message.channel.send("https://media.discordapp.net/attachments/541361310021976074/901234009227550750/giphy.gif")
        return True
    return False