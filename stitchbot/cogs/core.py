"""Core commands shipped with StitchBot."""

from __future__ import annotations

import platform
import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from ..bot import StitchBot


class Core(commands.Cog):
    """Basic informational commands."""

    def __init__(self, bot: "StitchBot") -> None:
        self.bot = bot
        self._boot_time = time.monotonic()

    @commands.hybrid_command(description="Return a simple healthcheck message.")
    async def ping(self, ctx: commands.Context) -> None:
        """Reply with the bot latency."""

        latency_ms = round(self.bot.latency * 1000)
        await ctx.reply(f"🏓 Pong! Latency: {latency_ms}ms", mention_author=False)

    @commands.hybrid_command(description="Display diagnostic information about StitchBot.")
    async def info(self, ctx: commands.Context) -> None:
        """Show basic diagnostic information."""

        uptime_seconds = int(time.monotonic() - self._boot_time)
        uptime_minutes, seconds = divmod(uptime_seconds, 60)
        uptime_hours, minutes = divmod(uptime_minutes, 60)
        uptime_days, hours = divmod(uptime_hours, 24)
        uptime = f"{uptime_days}d {hours}h {minutes}m {seconds}s"

        embed = discord.Embed(title="StitchBot", colour=discord.Colour.blurple())
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.add_field(name="Prefix", value=self.bot.command_prefix, inline=False)
        embed.add_field(name="Python", value=platform.python_version(), inline=False)
        embed.add_field(name="discord.py", value=discord.__version__, inline=False)
        await ctx.reply(embed=embed, mention_author=False)


__all__ = ["Core"]
