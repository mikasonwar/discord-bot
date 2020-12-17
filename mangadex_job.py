import mangadex 
import discord_bot
import database
import asyncio

DB = database.getDB()
bot = discord_bot.getBot()
manga_id = 4880 # https://mangadex.org/title/4880

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await job()

def getTrackedChapter():
    rows = DB(DB.config.key == "mangaChapter").select()
    if(len(rows)>0):
        return int(rows[0].value)
    else:
        chapter = getLastestChapter().cached_chapter
        DB.config.update_or_insert(DB.config.key == 'mangaChapter',
                           key='mangaChapter',
                           guild=0,
                           value=chapter)
        return int(chapter)
        

def getLastestChapter():
    result = [chapter for chapter in mangadex.Manga(manga_id).populate().get_chapters() if chapter.cached_lang_code == 'gb']
    chapter = result[0]
    return chapter

async def job():
    latest = getLastestChapter()
    if(getTrackedChapter() > int(getLastestChapter().cached_chapter)):
        manga = mangadex.Manga(manga_id).populate()
        await discord_bot.MangaDexNotification(format_chapter_name(latest), "https://mangadex.org/" + manga.cover_url, f"https://mangadex.org/chapter/{latest.id}")

    print("Bot is logging out...")
    await bot.logout()

def format_chapter_name(chapter):
    return f'Vol.{chapter.cached_volume} {chapter.cached_chapter} - {chapter.cached_title}'

discord_bot.start_bot()