from loguru import logger
import aiohttp
from app.core.database import get_session
from price_updater.clients.moex_client import MoexClient
from shared.repositories.asset_price import AssetPriceRepository
from app.schemas.asset_price import AssetPriceCreate
from app.core.database import async_session_maker
async def fetch_prices(moex: MoexClient):
    try:
        prices = await moex.get_all_prices()
        return prices
    except Exception as e:
        logger.error(f"!!!!!!! Ошибка при получении: {e} !!!!!!!")
        return None


async def update_prices(session, asset_registry):
    logger.info("****** Обновление цен *******")

    assets = asset_registry.get_all()
    if not assets:
        logger.warning("!!!!!! Нет активов для обновления !!!!!!")
        return
    connector = aiohttp.connector.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as http_session:
        moex = MoexClient(session=http_session)
        try:
            prices = await moex.get_all_prices()
        except Exception as e:
            logger.error(f"!!!!!!! Ошибка при получении цен: {e} !!!!!!!")
            return

    for asset_id, ticker in assets.items():
        price = prices.get(ticker)
        if price is None:
            logger.warning(f"⚠ Нет цены для тикера {ticker}")
            continue
        async with async_session_maker() as session:
            repo = AssetPriceRepository(session=session)
            await repo.create(AssetPriceCreate(asset_id=asset_id, price=price, currency="RUB", source="moex"))
            logger.info(f"💰 {ticker}: {price}")

    await session.commit()
    logger.info("****** Обновление завершено ******")