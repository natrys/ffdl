import asyncio
import aiohttp

from bs4 import BeautifulSoup
from ebooklib import epub


async def getmetadata(session, story_url):
  async with session.get(story_url) as response:
    story = BeautifulSoup(await response.text(), "lxml")
    title = story.find("h1", attrs={"class": "Story__title"}).text
    author = story.find("div", attrs={"class": "Story__meta-author"}).a.text
    chapters = len(story.find("div", attrs={"class": "modal-body"})\
                   .ul.find_all("li"))
  return title, author, chapters


async def get_chapter(session, chapter_id, story_url):
  url = f"{story_url}/{chapter_id}"

  async with session.get(url) as response:
    chapter_text = \
      BeautifulSoup(await response.text(), "lxml")\
      .find("div", attrs = {"class": "StoryChapter__text"})

  chapter_text.contents[0].attrs = {"class": "Chapter"}
  chapter_node = epub.EpubHtml(title=f"Chapter {chapter_id:03}",
                               file_name=f"chap_{chapter_id:03}.xhtml",
                               lang='en')
  chapter_node.content = chapter_text.encode("utf-8")
  return chapter_node


async def fictionhunt(story_id):
  fictionhunt = "http://fictionhunt.com"
  story_url = f"{fictionhunt}/read/{story_id}"
  async with aiohttp.ClientSession() as session:
    title, author, total = await getmetadata(session, story_url)
    chapters = (get_chapter(session, chapter, story_url)
                for chapter in range(1, total + 1))
    return title, author, (await asyncio.gather(*chapters))
