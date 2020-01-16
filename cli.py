import plac, asyncio
from ffdl import *


def main(url_or_id: ("Fanfiction.net URL or just the ID")):
    story_id = get_id(url_or_id)
    asyncio.run(create_epub(story_id))


if __name__ == "__main__":
    plac.call(main, version=ffdl.__version__)
