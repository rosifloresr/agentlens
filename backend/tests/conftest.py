from collections.abc import AsyncIterator, Iterator
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from app.config import get_settings
from app.main import create_app

@pytest.fixture(autouse=True)
def _test_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()

@pytest.fixture
def app() -> FastAPI:
    return create_app()

@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c