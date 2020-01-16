import plac, asyncio
import ffdl


def main(url_or_id: ("Fanfiction.net URL or just the ID")):
    story_id = ffdl.get_id(url_or_id)
    asyncio.run(ffdl.create_epub(story_id))


if __name__ == "__main__":
    plac.call(main, version=ffdl.__version__)
