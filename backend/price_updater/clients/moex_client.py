from decimal import Decimal

import aiohttp
from price_updater.clients.exceptions import (
    MoexError,
    MoexHTTPError,
    MoexNetworkError,
    MoexParseError,
    MoexSessionNotOpened,
)


class MoexClient:
    URL_ALL = (
        'https://iss.moex.com/iss/engines/stock/markets/shares/securities.json'
        '?marketdata.columns=SECID,LAST'
    )

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def aopen(self) -> None:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                timeout=aiohttp.ClientTimeout(total=30),
            )

    async def aclose(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def get_all_prices(self) -> dict[str, Decimal]:
        if not self._session or self._session.closed:
            raise MoexSessionNotOpened('You forgot to call MoexClient aopen()')
        try:
            async with self._session.get(self.URL_ALL) as resp:
                if resp.status >= 400:
                    body = await resp.text()
                    raise MoexHTTPError(status=resp.status, body=body)
                data = await resp.json()
        except MoexHTTPError:
            raise
        except aiohttp.ClientError as e:
            raise MoexNetworkError(str(e)) from e
        except Exception as e:
            raise MoexError(str(e)) from e
        try:
            rows = data['marketdata']['data']
        except Exception as e:
            raise MoexParseError('Unexpected MOEX response schema') from e

        prices: dict[str, Decimal] = {}
        for secid, last in rows:
            if last is None:
                continue
            prices[secid] = Decimal(str(last))

        return prices

    async def get_security_info(self, ticker: str) -> dict:
        pass
