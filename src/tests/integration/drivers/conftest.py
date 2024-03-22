from typing import AsyncGenerator

from httpx import AsyncClient
import pytest

from drivers.rest.main import app


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
