import plac, re
import ffdl

def get_id(url):
  pattern = re.compile("(?:fanfiction\.net|fictionhunt\.com)/(?:s|read)/(\d+)")
  return int(re.search(pattern, url).group(1))

def main(url_or_id: ("Fanfiction.net URL or just the ID")):
  story_id = int(url_or_id) if url_or_id.isdigit() else get_id(url_or_id)
  ffdl.create_epub(story_id)

if __name__ == '__main__':
  plac.call(main, version=ffdl.__version__)
