# OctoberCMS Claude Code Plugin

A Claude Code plugin for OctoberCMS development with version-specific documentation and auto-sync.

## Features

- **Auto-Detect Version** - Automatically detects your OctoberCMS version via `php artisan october:about`
- **Global Documentation** - Docs stored at `~/.claude/octobercms-docs/` (shared across projects)
- **Community Answers** - 530+ solved topics from the official OctoberCMS forum as a searchable knowledge base
- **Auto-Sync** - Checks for doc and community answer updates on every session start
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
  "last_sync": "2026-02-01T00:00:00Z",
  "auto_sync": true,
  "auto_sync_mode": "auto",
  "community_answers": true
}
```

### Auto-Sync Modes

| Mode | Description |
|------|-------------|
| `auto` | Sync automatically on session start if updates available |
| `notify` | Just notify when updates available |
| `off` | Never check automatically |

## Documentation Storage

- **Global:** `~/.claude/octobercms-docs/` and `~/.claude/octobercms-community-answers/`
- **Versions:** Downloaded on-demand (only what you need)
- **Shared:** All projects use the same docs (no duplication)

```
~/.claude/
├── octobercms-docs/
│   ├── 3.x/          # Downloaded when needed
│   ├── 4.x/          # Downloaded when needed
│   └── .git-hash     # For sync tracking
└── octobercms-community-answers/
    ├── need-help/     # 530+ solved topics
    ├── questions/
    ├── tips-and-tricks/
    └── known-issues/
```

## Skills (Auto-Invoked)

The plugin includes a skill that Claude automatically uses:

- **octobercms-core** - Build order, artisan commands, best practices, community answer search

The skill auto-triggers via `.claude/CLAUDE.md` (added during setup) and context detection.

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
