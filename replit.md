# StitchBot - Discord Bot Project

## Overview
StitchBot is a Discord automation bot designed to provide a lightweight foundation for community management. The bot includes a modular cog system with demonstration commands and a production-ready configuration loader.

## Project Structure
```
stitchbot/
├── cogs/              # Modular command cogs
│   ├── core.py        # Basic commands (ping, info)
│   └── verification.py # Verification features
├── bot.py             # Main bot implementation
├── cli.py             # Command-line interface
└── config.py          # Configuration loader
```

## Technology Stack
- **Language**: Python 3.10+
- **Framework**: discord.py 2.3.2+
- **Build System**: hatchling
- **Package Manager**: uv

## Configuration
The bot uses environment variables with the `STITCHBOT_` prefix:

- `STITCHBOT_TOKEN` (required): Discord bot token
- `STITCHBOT_PREFIX` (optional): Command prefix (default: `/`)
- `STITCHBOT_GUILD` (optional): Guild ID to restrict bot interactions

## Available Commands
- `/ping` - Returns bot latency healthcheck
- `/info` - Displays diagnostic information (uptime, version, etc.)

## Running in Replit
The bot runs automatically via the `stitchbot` workflow which executes the CLI entrypoint. The workflow is configured to run in console mode and will automatically restart when changes are made to the code.

## Development
- Run tests: `pytest`
- Dry-run config validation: `stitchbot --dry-run`
- Custom log level: `stitchbot --log-level DEBUG`

## Recent Changes
- **2025-11-10**: Initial import and setup in Replit environment
  - Installed dependencies using uv package manager
  - Configured STITCHBOT_TOKEN secret
  - Created workflow to run the bot automatically
  - Bot successfully connected to Discord Gateway

## Features
- Structured configuration via environment variables
- Modular cog system for easy extension
- Hybrid commands supporting both prefix and slash commands
- Type-annotated codebase
- Unit test coverage
