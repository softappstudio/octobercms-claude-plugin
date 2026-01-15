# OctoberCMS Claude Code Plugin

A Claude Code plugin for OctoberCMS development with version-specific documentation and skills.

## Features

- 🔧 **Interactive Setup** - Configure your OctoberCMS version with `/setup`
- 📚 **Local Documentation** - Clone and search official docs locally
- 🔄 **Auto-Sync** - Automatically checks for doc updates on session start
- 🎯 **Version-Specific Skills** - Automatic guidance based on your version
- 🔍 **Quick Search** - Find docs fast with `/october <topic>`

## Installation

### From Marketplace (when published)

```bash
/plugin install octobercms@your-marketplace
```

### Local Development

```bash
# Clone this repository
git clone https://github.com/your-org/octobercms-claude-plugin.git

# Create a local marketplace
mkdir my-marketplace/.claude-plugin
echo '{"name": "my-marketplace", "owner": {"name": "Dev"}, "plugins": [{"name": "octobercms", "source": "./octobercms-claude-plugin"}]}' > my-marketplace/.claude-plugin/marketplace.json

# In Claude Code
/plugin marketplace add ./my-marketplace
/plugin install octobercms@my-marketplace
```

## Commands

| Command | Description |
|---------|-------------|
| `/setup` | Interactive setup - select version and download docs |
| `/sync-docs` | Manually update local documentation from GitHub |
| `/sync-settings` | Configure auto-sync behavior (mode, interval, etc.) |
| `/october <topic>` | Search documentation for a topic |
| `/october-version <ver>` | Switch to a different OctoberCMS version |

## Skills (Auto-Invoked)

The plugin includes skills that Claude automatically uses when relevant:

- **octobercms-core** - General OctoberCMS development guidance
- **octobercms-backend** - Backend forms, lists, relations, controllers
- **octobercms-frontend** - CMS pages, components, themes, AJAX

## Quick Start

1. Install the plugin
2. Run `/setup` in your project
3. Select your OctoberCMS version (4.x, 3.x, 2.x, or 1.x)
4. Start coding! Ask questions like:
   - "How do I create a backend form?"
   - "Show me the component structure"
   - "What's the AJAX syntax for this version?"

## Configuration

Configuration is stored in `.claude/octobercms-config.json`:

```json
{
  "version": "4.x",
  "docs_path": ".claude/octobercms-docs/4.x",
  "last_sync": "2024-01-15T10:30:00Z",
  "commit_hash": "abc1234...",
  "repo_url": "https://github.com/octobercms/docs",
  "branch": "develop",
  "auto_sync": true,
  "auto_sync_mode": "auto",
  "auto_sync_interval_days": 7,
  "auto_sync_silent": false
}
```

### Auto-Sync Options

| Option | Values | Description |
|--------|--------|-------------|
| `auto_sync` | `true`/`false` | Enable automatic update checking |
| `auto_sync_mode` | `"auto"`, `"notify"`, `"off"` | What to do when updates found |
| `auto_sync_interval_days` | `1-30` | Days between update checks |
| `auto_sync_silent` | `true`/`false` | Only show output when updates available |

**Modes:**
- **auto** - Automatically download and install updates
- **notify** - Just inform you updates are available (run `/sync-docs` manually)
- **off** - Never check automatically

## Supported Versions

| Version | Laravel | PHP | Status |
|---------|---------|-----|--------|
| 4.x | 11 | 8.2+ | ✅ Current |
| 3.x | 9 | 8.0+ | ✅ Stable |
| 2.x | 6 | 7.4+ | ⚠️ Legacy |
| 1.x | 5 | 7.0+ | ⚠️ Legacy |

## License

MIT
