import os
from collections.abc import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from app.core.database import get_session
from app.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def _test_db_url() -> str:
    return os.environ['TEST_DATABASE_URL']  # теперь обязательно задаём для Alembic


def _alembic_config() -> Config:
    cfg = Config('alembic.ini')
    cfg.set_main_option('sqlalchemy.url', _test_db_url())
    return cfg


@pytest.fixture(scope='session')
async def engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(_test_db_url(), future=True)

    command.upgrade(_alembic_config(), 'head')

    try:
        yield engine
    finally:
        command.downgrade(_alembic_config(), 'base')
        await engine.dispose()


@pytest.fixture
async def db_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with engine.connect() as conn:
        trans = await conn.begin()
        Session = async_sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False)
        session = Session()
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def _override_get_session() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac

    app.dependency_overrides.clear()
