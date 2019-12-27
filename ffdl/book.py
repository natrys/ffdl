import time, logging, sys
import asyncio

from ebooklib import epub
from ffdl import fictionhunt

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr
)

def create_epub(story_id):
  logger = logging.getLogger(__name__)
  start = time.perf_counter()

  book = epub.EpubBook()
  title, author, chapters = asyncio.run(fictionhunt(story_id))
  logger.debug(f"Download finished after: {time.perf_counter() - start} seconds")

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

  bookname = f'{author} - {title}'
  epub.write_epub(f'{bookname}.epub', book)

  logger.info(f"Book created after: {time.perf_counter() - start} seconds")
  print(f"{bookname}.epub created")
