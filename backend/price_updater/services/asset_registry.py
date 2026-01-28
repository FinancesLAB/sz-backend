from app.repositories import AssetRepositoryPostgres


class AssetRegistry:
    def __init__(self):
        self.assets: dict[int, str] = {}

    async def load(self, session):
        repo = AssetRepositoryPostgres(session=session)
        rows = await repo.get_all(limit=250, offset=0)
        self.assets = {row.id: row.ticker for row in rows}

    def get_all(self) -> dict:
        return self.assets

    def get_ticker(self, asset_id: int) -> str:
        return self.assets.get(asset_id)
