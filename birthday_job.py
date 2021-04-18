import discord_job
import discord
import database
import asyncio
import utils_mikas
from datetime import datetime

DB = database.getDB()
bot = discord_job.DiscordJob("Birthday Checker", True)
date_to_search = datetime.today().strftime('%d/%m')

print(date_to_search)

class BirthdayJob(object):
    def __init__(self):
        self.rows = DB(DB.birthdays.birthday == date_to_search).select()

birthday_job = BirthdayJob()

async def job(fun):
    rows = DB(DB.birthdays.birthday == date_to_search).select()
    for row in rows:
        await fun(content=f"O <@{row.user_id}> faz anos hoje! \n\n Tudo a dar-lhe os parabéns! \n @everyone")


if birthday_job.rows:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.send_message_to_bound_channels(job))

bot.run()