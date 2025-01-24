import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pytest_asyncio import is_async_test


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def client():
    return AsyncIOMotorClient("mongodb://localhost:27017")
