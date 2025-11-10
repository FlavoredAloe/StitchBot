"""Console script for running StitchBot."""

from __future__ import annotations

import argparse
import logging
import sys

from .config import ConfigurationError, load_settings
from .bot import run


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the StitchBot Discord bot")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration and exit without connecting to Discord.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Configure the log level (default: INFO).",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.log_level)

    try:
        settings = load_settings()
    except ConfigurationError as exc:
        logging.getLogger(__name__).error("Configuration error: %s", exc)
        return 1

    if args.dry_run:
        logging.getLogger(__name__).info(
            "Configuration valid. Prefix=%s guild=%s",
            settings.command_prefix,
            settings.guild_id or "<any>",
        )
        return 0

    run(settings)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
