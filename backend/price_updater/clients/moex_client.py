import aiohttp
from loguru import logger


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

    async def get_all_prices(self) -> dict[str, float]:
        if not self._session or self._session.closed:
            raise
        try:
            async with self._session.get(self.URL_ALL) as resp:
                # советую добавить, чтобы не парсить html/ошибки как json
                resp.raise_for_status()
                data = await resp.json()
        except Exception as e:
            logger.error(f'!!!!!! Ошибка сети: {e} !!!!!')
            raise

        prices: dict[str, float] = {}
        for secid, last in data['marketdata']['data']:
            if last is None:
                continue
            prices[secid] = float(last)

        return prices

    async def get_security_info(self, ticker: str) -> dict:
        pass
