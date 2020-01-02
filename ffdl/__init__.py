__version__ = '0.1.0'

import re

from ffdl.utils import cd
from ffdl.book import create_epub

def get_id(url_or_id):
  if url_or_id.isdigit():
    return int(url_or_id)
  else:
    pattern = re.compile("(?:fanfiction\.net|fictionhunt\.com)/(?:s|read)/(\d+)")
    return int(re.search(pattern, url_or_id).group(1))
