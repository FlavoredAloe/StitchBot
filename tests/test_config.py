from __future__ import annotations

from pathlib import Path

import pytest

from stitchbot.config import ConfigurationError, load_settings


def test_load_settings_requires_token(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("STITCHBOT_PREFIX=?\n")

    with pytest.raises(ConfigurationError):
        load_settings(env_paths=(env_file,))


def test_load_settings_reads_values(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "STITCHBOT_TOKEN=token",
                "STITCHBOT_PREFIX=$",
                "STITCHBOT_GUILD=1234",
            ]
        )
    )

    settings = load_settings(env_paths=(env_file,))

    assert settings.token == "token"
    assert settings.command_prefix == "$"
    assert settings.guild_id == 1234


def test_load_settings_handles_invalid_guild(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "STITCHBOT_TOKEN=token",
                "STITCHBOT_GUILD=not-a-number",
            ]
        )
    )

    with pytest.raises(ConfigurationError):
        load_settings(env_paths=(env_file,))
