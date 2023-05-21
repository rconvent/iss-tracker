import asyncio
from typing import Any, AsyncGenerator, Generator

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from async_asgi_testclient import TestClient
from fastapi import FastAPI


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    from src.main import app

    host, port = "127.0.0.1", "9000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client
