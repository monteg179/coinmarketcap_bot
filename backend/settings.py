import logging
import os

from dotenv import (
    load_dotenv,
)

LOG_LEVEL = logging.INFO

JOB_INTERVAL = 900.0
COIN_MARKET_CAP_INTERVAL = 300.0


class Enviroment:

    TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
    WEBHOOK_PORT = 'WEBHOOK_PORT'
    WEBHOOK_URL = 'WEBHOOK_URL'
    WEBHOOK_SECRET = 'WEBHOOK_SECRET'
    WEBHOOK_PATH = 'WEBHOOK_PATH'
    WEBHOOK_CERT = 'WEBHOOK_CERT'
    COIN_MARKET_CAP = 'COIN_MARKET_CAP'

    def __init__(self) -> None:
        load_dotenv()
        self.__telegram_token = os.getenv(type(self).TELEGRAM_TOKEN)
        self.__webhook_port = int(os.getenv(type(self).WEBHOOK_PORT, 0))
        self.__webhook_url = os.getenv(type(self).WEBHOOK_URL)
        self.__webhook_secret = os.getenv(type(self).WEBHOOK_SECRET)
        self.__webhook_path = os.getenv(type(self).WEBHOOK_PATH, '')
        self.__webhook_cert = os.getenv(type(self).WEBHOOK_CERT)
        self.__coin_market_cap = os.getenv(type(self).COIN_MARKET_CAP)

    @property
    def telegram_token(self) -> str:
        return self.__telegram_token

    @property
    def webhook_url(self) -> str | None:
        return self.__webhook_url

    @property
    def webhook_port(self) -> int | None:
        return self.__webhook_port

    @property
    def webhook_secret(self) -> str | None:
        return self.__webhook_secret

    @property
    def webhook_path(self) -> str | None:
        return self.__webhook_path

    @property
    def webhook_cert(self) -> str | None:
        return self.__webhook_cert

    @property
    def coin_market_cap(self) -> str:
        return self.__coin_market_cap


enviroment = Enviroment()
