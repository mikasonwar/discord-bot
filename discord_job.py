import discord
import os
import libs.logger as logger
import asyncio
import libs.database as database
from dotenv import load_dotenv
import settings

logger = logger.Logger("logs", "jobs")
DB = database.getDB()

# Não estou nada feliz com esta merda puta que pariu a minha vida
# Pelo menos tenho algo para poder chamar os jobs e mandar uma mensagem

class DiscordJob(object):
    
    def __init__(self,jobName, mikas_only = False):
        self.bot = discord.Client()
        self.jobName = jobName
        self.pending = []
        self.mikas_only = mikas_only
        self.write_to_logs("Starting job...")

    async def on_ready(self):
        self.write_to_logs(f'{self.bot.user} has connected to Discord!')
        for fun in self.pending:
            await fun.task(fun.cb)
        
        await self.bot.close()

    async def on_disconnect(self):
        self.write_to_logs(f'Disconnecting...')
        # exit()

    async def send_message_to_bound_channels(self,cb):
        result = lambda: None
        result.task = self._send_message_to_bound_channels
        result.cb = cb
        self.pending.append(result)

    def write_to_logs(self,message):
        logger.info(f"{message} [Job: {self.jobName}]")

    async def _send_message_to_bound_channels(self, cb):
        if self.mikas_only:
            rows = DB(DB.config.key == "bindedChannel", DB.config.guild == settings.mikas_guild).select()
            for row in rows:
                channel_id = row.value
                channel = self.bot.get_channel(int(channel_id))

                task = asyncio.create_task(cb(channel.send))
                await task
                self.write_to_logs(f'Sent message to mikas channel')
        else:
            rows = DB(DB.config.key == "bindedChannel").select()
            for row in rows:
                channel_id = row.value
                channel = self.bot.get_channel(int(channel_id))

                task = asyncio.create_task(cb(channel.send))
                await task
                self.write_to_logs(f'Sent message to bound channels')


    def run(self):
        self.bot.event(self.on_ready)
        self.bot.event(self.on_disconnect)
        if self.pending:
            self.write_to_logs(f'Running pending jobs ({len(self.pending)})')
            self.bot.run(settings.token)
        else:
            self.write_to_logs(f'Nothing to do...')



    