"""RoVer API integration helpers."""

from __future__ import annotations

from dataclasses import dataclass

import aiohttp

__all__ = [
    "RoVerClient",
    "RoVerError",
    "RoVerProfile",
    "RoVerServiceError",
    "RoVerUserNotFoundError",
]


@dataclass(slots=True)
class RoVerProfile:
    """Representation of a Roblox user linked through RoVer."""

    roblox_id: int
    roblox_username: str
    roblox_display_name: str | None = None


class RoVerError(RuntimeError):
    """Base exception raised for RoVer related failures."""


class RoVerServiceError(RoVerError):
    """Raised when RoVer responds with an error state."""


class RoVerUserNotFoundError(RoVerError):
    """Raised when no RoVer verification exists for a Discord user."""


class RoVerClient:
    """Simple API client for interacting with RoVer."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        session: aiohttp.ClientSession | None = None,
        base_url: str = "https://registry.rover.link/api",
    ) -> None:
        self._api_key = api_key
        self._session: aiohttp.ClientSession | None = session
        self._owns_session = session is None
        self._base_url = base_url.rstrip("/")

    @property
    def base_url(self) -> str:
        return self._base_url

    async def close(self) -> None:
        """Close the underlying :mod:`aiohttp` session if owned."""

        if self._owns_session and self._session and not self._session.closed:
            await self._session.close()

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def fetch_profile(self, discord_id: int) -> RoVerProfile:
        """Fetch the RoVer profile linked to a Discord user."""

        session = self._get_session()
        url = f"{self._base_url}/user/{discord_id}"
        
        headers = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 404:
                    raise RoVerUserNotFoundError(
                        "No Roblox account is linked to this Discord user via RoVer."
                    )
                if response.status >= 400:
                    raise RoVerServiceError(
                        f"RoVer responded with HTTP {response.status}."
                    )

                payload = await response.json()
        except aiohttp.ContentTypeError as exc:
            raise RoVerServiceError("RoVer returned an invalid payload.") from exc
        except aiohttp.ClientError as exc:  # pragma: no cover - network error guard
            raise RoVerError("Failed to communicate with RoVer.") from exc

        status = payload.get("status")
        if status != "ok":
            message = payload.get("error", "Unexpected response from RoVer.")
            raise RoVerServiceError(message)

        try:
            roblox_id = int(payload["robloxId"])
            roblox_username = str(payload["robloxUsername"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RoVerServiceError("Received malformed payload from RoVer.") from exc

        display_name = payload.get("robloxDisplayName")
        if display_name is not None:
            display_name = str(display_name)

        return RoVerProfile(
            roblox_id=roblox_id,
            roblox_username=roblox_username,
            roblox_display_name=display_name,
        )
