import time, logging
import asyncio

from ebooklib import epub
from ffdl.fictionhunt import fictionhunt
from ffdl.utils import logger


async def create_epub(story_id):
  start = time.perf_counter()
  logger.info("Starting Download")

  book = epub.EpubBook()
  title, author, chapters = await fictionhunt(story_id)
  logger.info(f"Download finished after: {time.perf_counter() - start} seconds")

  book.set_identifier(f"{story_id}")
  book.set_title(title)
  book.add_author(author)
  book.set_language('en')

  for index, chapter_node in enumerate(chapters):
    book.add_item(chapter_node)

  book.toc = (chapters)

  style = '''
@namespace epub "http://www.idpf.org/2007/ops";
body {
    font-family: Liberation Serif, Helvetica, Times New Roman, serif;
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
'''

  nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css",
                          media_type="text/css", content=style)

  book.add_item(nav_css)
  book.spine = ['nav'] + chapters

  book.add_item(epub.EpubNcx())
  book.add_item(epub.EpubNav())

  bookname = f'{author} - {title}.epub'
  epub.write_epub(f'{bookname}', book)

  logger.info(f"Book created after: {time.perf_counter() - start} seconds")
  return bookname
