import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

import pytest


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client():
    return AsyncIOMotorClient("mongodb://localhost:27017")
