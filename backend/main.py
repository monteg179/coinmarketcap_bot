import logging

from backend.bot import (
    run_bot,
)
from backend import settings

LOG_LEVEL = settings.LOG_LEVEL

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)
logging.getLogger('httpx').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main():
    run_bot()


if __name__ == '__main__':
    main()
