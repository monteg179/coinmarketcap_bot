from typing import (
    Any,
)

import httpx

from backend import settings


class CoinMarketCapClient:

    URL = ('https://pro-api.coinmarketcap.com'
           '/v1/cryptocurrency/listings/latest')

    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.__client = httpx.AsyncClient()
        self.__coins = {}
        self.__prices = {}

    async def cryptocurrency(self) -> None:
        response = await self.__client.get(
            url=type(self).URL,
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': self.__api_key,
            },
            params={
                'convert': 'USD'
            }
        )
        if response.status_code == httpx.codes.OK:
            self.parsing(response.json())

    def parsing(self, json: dict[str, Any]) -> None:
        coins = {}
        prices = {}
        for item in json.get('data'):
            symbol = item['symbol'].upper()
            name = item['name']
            price = item['quote']['USD']['price']
            coins[symbol] = name
            prices[symbol] = price
        self.__coins = coins
        self.__prices = prices

    async def close(self) -> None:
        await self.__client.aclose()

    @property
    def coins(self) -> dict[str, str]:
        return self.__coins

    @property
    def prices(self) -> dict[str, float]:
        return self.__prices


coin_market_cap_client = CoinMarketCapClient(
    api_key=settings.enviroment.coin_market_cap,
)
