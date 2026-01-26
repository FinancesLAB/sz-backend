import pytest

pytestmark = pytest.mark.asyncio


async def test_openapi_available(client):
    r = await client.get('/openapi.json')
    assert r.status_code == 200
