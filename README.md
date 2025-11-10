# StitchBot

StitchBot is a Discord bot designed to provide a lightweight foundation for
automation and community management. The project includes a production-ready
configuration loader, a CLI entrypoint, and a small set of demonstration cogs to
help you get started quickly.

## Features

- 🔧 Structured configuration via environment variables (`STITCHBOT_*`).
- 🤖 `StitchBot` subclass with sensible default Discord intents.
- 🧩 Modular cog system with an example `ping` and `info` command.
- 🧪 Unit tests covering configuration parsing edge cases.

## Getting started

1. Install dependencies and StitchBot in editable mode:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Create a Discord application and bot token. Copy the token into a `.env`
   file:

   ```env
   STITCHBOT_TOKEN=your_bot_token
   STITCHBOT_PREFIX=!
   STITCHBOT_GUILD=123456789012345678  # optional: restrict interactions to a guild
   ```

3. Run the bot using the provided CLI:

   ```bash
   stitchbot
   ```

   Use the `--dry-run` flag to validate configuration without connecting to
   Discord.

## Development

Run the unit tests with `pytest`:

```bash
pytest
```

StitchBot ships with type annotations throughout the codebase. Tools such as
`pyright` or `mypy` can be introduced with minimal setup if desired.
