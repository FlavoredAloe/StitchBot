"""Commands related to Roblox verification via RoVer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ..rover import RoVerClient, RoVerError, RoVerProfile, RoVerUserNotFoundError

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from ..bot import StitchBot


class Verification(commands.Cog):
    """Provide commands that surface RoVer verification details."""

    def __init__(self, bot: "StitchBot", *, rover: RoVerClient | None = None) -> None:
        self.bot = bot
        self._rover = rover or RoVerClient()

    async def cog_unload(self) -> None:  # pragma: no cover - discord teardown
        await self._rover.close()

    @commands.hybrid_command(description="Look up a member's RoVer verification status.")
    async def verify(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        """Display Roblox account information for *member* via RoVer."""

        target = member or ctx.author

        try:
            profile = await self._rover.fetch_profile(target.id)
        except RoVerUserNotFoundError:
            await ctx.reply(
                f"{target.mention} has not linked a Roblox account through RoVer.",
                mention_author=False,
            )
            return
        except RoVerError:
            await ctx.reply(
                "Unable to contact RoVer right now. Please try again later.",
                mention_author=False,
            )
            return

        embed = self._build_embed(target, profile)
        await ctx.reply(embed=embed, mention_author=False)

    def _build_embed(self, member: discord.Member, profile: RoVerProfile) -> discord.Embed:
        embed = discord.Embed(
            title=f"RoVer verification for {member.display_name}",
            colour=discord.Colour.green(),
        )
        embed.add_field(name="Roblox Username", value=profile.roblox_username, inline=False)
        embed.add_field(name="Roblox ID", value=str(profile.roblox_id), inline=False)
        if profile.roblox_display_name:
            embed.add_field(
                name="Roblox Display Name",
                value=profile.roblox_display_name,
                inline=False,
            )
        embed.set_thumbnail(
            url=(
                "https://www.roblox.com/headshot-thumbnail/image"
                f"?userId={profile.roblox_id}&width=420&height=420&format=png"
            )
        )
        embed.set_footer(text="Data provided by RoVer (verify.eryn.io)")
        return embed


__all__ = ["Verification"]
