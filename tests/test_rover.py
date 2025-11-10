"""Tests for the RoVer API integration layer."""

from __future__ import annotations

import asyncio

import pytest

from stitchbot.rover import (
    RoVerClient,
    RoVerProfile,
    RoVerServiceError,
    RoVerUserNotFoundError,
)


class _StubResponse:
    def __init__(self, *, status: int, payload: dict[str, object]) -> None:
        self.status = status
        self._payload = payload

    async def json(self) -> dict[str, object]:  # pragma: no cover - simple passthrough
        return self._payload

    async def __aenter__(self) -> "_StubResponse":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class _StubSession:
    def __init__(self, response: _StubResponse) -> None:
        self._response = response
        self.closed = False
        self.requested_urls: list[str] = []

    def get(self, url: str) -> _StubResponse:
        self.requested_urls.append(url)
        return self._response

    async def close(self) -> None:  # pragma: no cover - trivial
        self.closed = True


def run(coro):
    return asyncio.run(coro)


def test_fetch_profile_success() -> None:
    response = _StubResponse(
        status=200,
        payload={
            "status": "ok",
            "robloxId": 1234,
            "robloxUsername": "Builderman",
            "robloxDisplayName": "Builderman",
        },
    )
    session = _StubSession(response)
    client = RoVerClient(session=session)

    profile = run(client.fetch_profile(42))

    assert profile == RoVerProfile(
        roblox_id=1234,
        roblox_username="Builderman",
        roblox_display_name="Builderman",
    )
    assert session.requested_urls == ["https://verify.eryn.io/api/user/42"]


def test_fetch_profile_not_found() -> None:
    response = _StubResponse(status=404, payload={"status": "error", "error": "Not found"})
    client = RoVerClient(session=_StubSession(response))

    with pytest.raises(RoVerUserNotFoundError):
        run(client.fetch_profile(9001))


def test_fetch_profile_service_error() -> None:
    response = _StubResponse(status=200, payload={"status": "error", "error": "rate limited"})
    client = RoVerClient(session=_StubSession(response))

    with pytest.raises(RoVerServiceError):
        run(client.fetch_profile(999))


def test_fetch_profile_http_error_status() -> None:
    response = _StubResponse(status=429, payload={})
    client = RoVerClient(session=_StubSession(response))

    with pytest.raises(RoVerServiceError):
        run(client.fetch_profile(101))
