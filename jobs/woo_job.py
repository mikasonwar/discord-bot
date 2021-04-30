import fix_path
fix_path.fix()

import discord_job
import discord
import asyncio
import libs.utils_mikas as utils_mikas



bot = discord_job.DiscordJob("Woo Wednesday")

async def job(fun):
    file = discord.File(utils_mikas.getRandomFileFromPath('woo'))
    await fun(content="It's woo wednesday! WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", file=file)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.send_message_to_bound_channels(job))
bot.run()