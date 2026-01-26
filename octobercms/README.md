# OctoberCMS Claude Code Plugin

A Claude Code plugin for OctoberCMS development with version-specific documentation and auto-sync.

## Features

- **Auto-Detect Version** - Automatically detects your OctoberCMS version via `php artisan october:about`
- **Global Documentation** - Docs stored at `~/.claude/octobercms-docs/` (shared across projects)
- **Auto-Sync** - Checks for doc updates on every session start
- **On-Demand Downloads** - Only downloads versions you need
- **Version Switching** - Easily switch between 1.x, 2.x, 3.x, 4.x

## Installation

### For Development/Testing

```bash
claude --plugin-dir /path/to/octobercms-claude-plugin/octobercms
```

### From Marketplace (when published)

```bash
/plugin marketplace add softappstudio/octobercms-claude-plugin
/plugin install octobercms@softappstudio
```

## Commands

| Command | Description |
|---------|-------------|
| `/octobercms:setup` | Interactive setup - auto-detect version, download docs |
| `/octobercms:sync-docs` | Manually sync documentation from GitHub |
| `/octobercms:october-version [ver]` | Switch to a different OctoberCMS version |
| `/octobercms:update-settings` | Change auto-sync settings |

## Quick Start

1. Install the plugin
2. Run `/octobercms:setup` in your OctoberCMS project
3. It auto-detects your version and downloads the docs
4. Start coding with version-specific documentation!

## Configuration

Per-project config stored in `.claude/octobercms-config.json`:

```json
{
  "version": "4.x",
  "last_sync": "2026-01-19T12:00:00Z",
  "auto_sync": true,
  "auto_sync_mode": "auto"
}
```

### Auto-Sync Modes

| Mode | Description |
|------|-------------|
| `auto` | Sync automatically on session start if updates available |
| `notify` | Just notify when updates available |
| `off` | Never check automatically |

## Documentation Storage

- **Global:** `~/.claude/octobercms-docs/`
- **Versions:** Downloaded on-demand (only what you need)
- **Shared:** All projects use the same docs (no duplication)

```
~/.claude/octobercms-docs/
├── 3.x/          # Downloaded when needed
├── 4.x/          # Downloaded when needed
└── .git-hash     # For sync tracking
```

## Skills (Auto-Invoked)

The plugin includes a skill that Claude automatically uses:

- **octobercms-core** - Build order, artisan commands, best practices

The skill auto-triggers based on context (OctoberCMS files, directories, mentions).

## Supported Versions

| Version | Status |
|---------|--------|
| 4.x | Current |
| 3.x | Stable |
| 2.x | Legacy |
| 1.x | Legacy |

## License

MIT

## Author

SoftApp Studio - https://www.softappstudio.com
