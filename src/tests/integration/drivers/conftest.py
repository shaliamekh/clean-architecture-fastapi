from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from drivers.rest.main import app


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
