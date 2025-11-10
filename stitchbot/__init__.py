"""Top-level package for StitchBot."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import only for type checking
    from .config import BotSettings
    from .bot import StitchBot

__all__ = ["create_bot"]


def create_bot(*, settings: "BotSettings | None" = None) -> "StitchBot":
    from .bot import create_bot as _create_bot

    return _create_bot(settings=settings)
