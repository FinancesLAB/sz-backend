from sqlalchemy import select
from loguru import logger
from shared.repositories.asset import AssetRepository


class AssetRegistry:
    def __init__(self):
        self.assets: dict[int, str] = {}

    async def load(self, session):
        logger.info("**** загрузка список активов из БД ****")
        repo = AssetRepository(session=session)
        rows = await repo.get_all()
        self.assets = {row.id: row.ticker for row in rows}

    def get_all(self) -> dict:
        return self.assets

    def get_ticker(self, asset_id: int) -> str:
        return self.assets.get(asset_id)
