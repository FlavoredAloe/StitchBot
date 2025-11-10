"""Configuration helpers for StitchBot."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


DEFAULT_ENV_PATHS = (
    Path(".env"),
    Path.home() / ".stitchbot" / "bot.env",
)


@dataclass
class BotSettings:
    """Container for bot configuration."""

    token: str
    guild_id: Optional[int] = None
    command_prefix: str = "/"


class ConfigurationError(RuntimeError):
    """Raised when the configuration is invalid or incomplete."""


def _load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs from *path* into the environment."""

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()


def load_settings(*, env_paths: tuple[Path, ...] = DEFAULT_ENV_PATHS) -> BotSettings:
    """Load bot settings from environment variables.

    Parameters
    ----------
    env_paths:
        Paths that should be inspected for a ``.env`` file. The first
        existing file will be loaded.

    Returns
    -------
    BotSettings
        A populated settings object ready to be used when instantiating
        the Discord bot.

    Raises
    ------
    ConfigurationError
        If a required configuration value is missing.
    """

    for path in env_paths:
        if path.is_file():
            _load_env_file(path)
            break

    token = os.getenv("STITCHBOT_TOKEN")
    if not token:
        raise ConfigurationError("STITCHBOT_TOKEN is required to start the bot.")

    guild = os.getenv("STITCHBOT_GUILD")
    guild_id: Optional[int]
    if guild:
        try:
            guild_id = int(guild)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ConfigurationError("STITCHBOT_GUILD must be an integer if provided.") from exc
    else:
        guild_id = None

    prefix = os.getenv("STITCHBOT_PREFIX", "/")

    return BotSettings(token=token, guild_id=guild_id, command_prefix=prefix)


__all__ = ["BotSettings", "ConfigurationError", "load_settings"]
