---
description: Configure auto-sync settings for OctoberCMS documentation
allowed-tools: Bash, Write, Read
---

# Configure Sync Settings

Modify automatic documentation sync behavior without full re-setup.

## Current Settings

First, show current configuration:

```bash
cat .claude/octobercms-config.json
```

## Available Settings

Present these options to the user:

### 1. Auto-Sync Mode
- **auto** - Automatically download updates (recommended)
- **notify** - Just inform when updates available
- **off** - Never check automatically

### 2. Check Interval
How often to check for updates (in days):
- Quick: 1 day
- Normal: 7 days (default)
- Relaxed: 14 days
- Minimal: 30 days

### 3. Silent Mode
- **On** - Only show messages when updates are found
- **Off** - Always show doc status on session start

## Update Configuration

After user makes selections, update the config file:

```bash
# Read current config, update fields, write back
python3 -c "
import json
with open('.claude/octobercms-config.json', 'r') as f:
    config = json.load(f)

config['auto_sync'] = ${AUTO_SYNC}  # true or false
config['auto_sync_mode'] = '${MODE}'  # 'auto', 'notify', or 'off'
config['auto_sync_interval_days'] = ${INTERVAL}  # 1-30
config['auto_sync_silent'] = ${SILENT}  # true or false

with open('.claude/octobercms-config.json', 'w') as f:
    json.dump(config, f, indent=2)
print('✅ Settings updated!')
"
```

## Confirmation

Show updated settings and explain behavior:

```
✅ Sync settings updated!

Mode: auto
Check interval: Every 7 days
Silent mode: Off

Documentation will automatically update when you start a Claude Code session
(if updates are available and at least 7 days have passed since last check).
```
