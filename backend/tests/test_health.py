import socket
from collections.abc import AsyncIterator
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.exc import OperationalError

from app.db.session import get_session


class FakeSession:
    async def execute(self, *args: Any, **kwargs: Any) -> None:
        return None


class BrokenSession:
    def __init__(self, error: Exception) -> None:
        self._error = error

    async def execute(self, *args: Any, **kwargs: Any) -> None:
        raise self._error


async def test_liveness_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_readiness_ok_when_database_responds(app: FastAPI, client: AsyncClient) -> None:
    async def override() -> AsyncIterator[FakeSession]:
        yield FakeSession()

    app.dependency_overrides[get_session] = override

    response = await client.get("/health/ready")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "error",
    [
        OperationalError("SELECT 1", {}, Exception("connection reset")),
        ConnectionRefusedError("connection refused"),
        socket.gaierror(-2, "Name or service not known"),
    ],
    ids=["wrapped-by-sqlalchemy", "connection-refused", "dns-failure"],
)
async def test_readiness_503_when_database_is_down(
    app: FastAPI, client: AsyncClient, error: Exception
) -> None:
    async def override() -> AsyncIterator[BrokenSession]:
        yield BrokenSession(error)

    app.dependency_overrides[get_session] = override

    response = await client.get("/health/ready")

    assert response.status_code == 503
