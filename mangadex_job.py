import mangadex 
import discord_job
import database
import asyncio
import discord

DB = database.getDB()
bot = discord_job.DiscordJob("MangaDex JoJo Check")
# Nem justifica ter um valor no .env mas depois vê-se a necessidade
manga_id = 4880 # https://mangadex.org/title/4880


class MangaDexJob(object):
    def __init__(self):
        self.chapter_name = ""
        self.manga_cover = ""
        self.chapter_url = ""
        self.chapter_number = None
        self.job = False
        self.check_for_chapter()

    def getTrackedChapter(self):
        rows = DB(DB.config.key == "mangaChapter").select()
        if(len(rows)>0):
            return int(rows[0].value)
        else:
            chapter = self.getLastestChapter().cached_chapter
            DB.config.update_or_insert(DB.config.key == 'mangaChapter',
                            key='mangaChapter',
                            guild=0,
                            value=chapter)
            DB.commit()
            return int(chapter)

    def getLastestChapter(self):
        result = [chapter for chapter in mangadex.Manga(manga_id).populate().get_chapters()]
        chapter = result[0]
        return chapter

    def check_for_chapter(self):
        latest = self.getLastestChapter()
        bot.write_to_logs(f"Tracked Chapter: {self.getTrackedChapter()}")
        bot.write_to_logs(f"Latest Chapter: {latest.cached_chapter}")
        if(self.getTrackedChapter() != int(latest.cached_chapter)):
            bot.write_to_logs("New Chapter detected... sending message")
            manga = mangadex.Manga(manga_id).populate()

            self.job = True
            self.chapter_number = latest.cached_chapter
            self.chapter_name = self.format_chapter_name(latest)
            self.manga_cover = f"https://mangadex.org/{manga.cover_url}"
            self.chapter_url = f"https://mangadex.org/chapter/{latest.id}"
        else:
            bot.write_to_logs("No new chapters")

    def updateTrackedChapter(self):
        DB.config.update_or_insert(DB.config.key == 'mangaChapter',
                            key='mangaChapter',
                            guild=0,
                            value=self.chapter_number)
        DB.commit()


    def format_chapter_name(self,chapter):
        return f'Vol.{chapter.cached_volume} {chapter.cached_chapter} - {chapter.cached_title}'

mangadex = MangaDexJob()

async def job(fun):
    mangadex.chapter_name
    embedVar = discord.Embed(title=mangadex.chapter_name, description="New Chapter", url=mangadex.chapter_url, color=0x00ff00)
    embedVar.set_footer(text="Made by Mikas™")
    embedVar.set_image(url=mangadex.manga_cover)
    embedVar.set_thumbnail(url=mangadex.manga_cover)
    mangadex.updateTrackedChapter()
    await fun(embed=embedVar)

if mangadex.job:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.send_message_to_bound_channels(job))


bot.run()