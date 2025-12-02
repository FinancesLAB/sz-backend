from sqlalchemy import select
from loguru import logger
from shared.models.asset import Asset

class AssetRegistry:
    def __init__(self):
        self.assets: dict[int, str] = {}

    async def load(self, session):
        logger.info("**** загрузка список активов из БД ****")
        result = await session.execute(select(Asset))
        rows = result.scalars().all()
        self.assets = {row.id: row.ticker for row in rows}

    def get_all(self):
        return self.assets

    def get_ticker(self, asset_id: int):
        return self.assets.get(asset_id)