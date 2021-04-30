import discord
import libs.utils_mikas as utils_mikas

async def handle(logger,message):
    await checkChad(logger,message)
    return True

async def checkChad(logger,message):
    if "chad" in message.content.lower().split(" "):
        logger.warning(f"{message.author} fired hasan event")
        file = discord.File(utils_mikas.getRandomFileFromPath('hasan'))
        await message.channel.send(file=file)
        return True
    return False