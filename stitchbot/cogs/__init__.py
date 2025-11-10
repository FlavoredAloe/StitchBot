"""Cog registration utilities for StitchBot."""

from __future__ import annotations

from typing import Iterable

from discord.ext import commands

from .core import Core
from .verification import Verification


def default_cogs() -> Iterable[type[commands.Cog]]:
    """Return the default set of cogs shipped with StitchBot."""

    return (Core, Verification)


async def register_default_cogs(bot: commands.Bot) -> None:
    """Register all default cogs on the provided bot instance."""

    for cog_cls in default_cogs():
        await bot.add_cog(cog_cls(bot))


__all__ = ["register_default_cogs", "default_cogs"]
