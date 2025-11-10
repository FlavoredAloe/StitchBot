"""Application entrypoint for StitchBot."""

from __future__ import annotations

import asyncio
import logging
from typing import Iterable, Sequence

import discord
from discord.ext import commands

from .config import BotSettings, load_settings

_logger = logging.getLogger(__name__)


def _default_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    return intents


class StitchBot(commands.Bot):
    """Discord bot implementation."""

    def __init__(self, *, settings: BotSettings, intents: discord.Intents | None = None) -> None:
        intents = intents or _default_intents()
        super().__init__(command_prefix=settings.command_prefix, intents=intents)
        self.settings = settings

    async def setup_hook(self) -> None:  # pragma: no cover - discord runs in event loop
        from .cogs import register_default_cogs

        await register_default_cogs(self)
        _logger.info("Loaded %s cogs", len(self.cogs))


async def run_bot(settings: BotSettings | None = None) -> None:
    """Start the StitchBot using asyncio."""

    settings = settings or load_settings()
    bot = StitchBot(settings=settings)
    async with bot:
        await bot.start(settings.token)


def create_bot(*, settings: BotSettings | None = None) -> StitchBot:
    """Create a configured instance of :class:`StitchBot`."""

    settings = settings or load_settings()
    return StitchBot(settings=settings)


def run(settings: BotSettings | None = None) -> None:
    """Synchronously run the bot in a blocking manner."""

    asyncio.run(run_bot(settings))


__all__ = ["StitchBot", "create_bot", "run", "run_bot"]
