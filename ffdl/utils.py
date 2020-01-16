import os, sys, logging


logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger(__name__)


def get_id(url_or_id):
    if url_or_id.isdigit():
        return int(url_or_id)
    else:
        pattern = re.compile("(?:fanfiction\.net|fictionhunt\.com)/(?:s|read)/(\d+)")
        return int(re.search(pattern, url_or_id).group(1))


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.makedirs(self.newPath, exist_ok=True)
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
