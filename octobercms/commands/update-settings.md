---
description: Update OctoberCMS plugin settings
allowed-tools: Bash, Read, Edit
---

# Update Settings

**CRITICAL INSTRUCTIONS:**
1. Run ALL bash commands silently - do NOT show command output to user
2. Do NOT ask for permission to update the config file - just do it
3. Only show the user-friendly messages specified below

## Step 1: Load Current Settings

Run silently:
```bash
test -f .claude/octobercms-config.json && cat .claude/octobercms-config.json || true
```

**If no config:** Show: `No configuration found. Run /octobercms:setup first.` and stop.

## Step 2: Show Settings Panel

Show current value and ask for new value:

```
Current: Auto-sync is [current mode]

Auto-sync documentation updates?

  1. Auto (recommended) - Sync on session start if updates available
  2. Notify - Notify on session start if updates available
  3. Off - Never check automatically
  4. Cancel - Keep current settings
```

**Auto is ALWAYS the recommended option**, regardless of current setting.

**If Cancel:** Show `Settings unchanged.` and stop.

## Step 3: Update Config

Update the config file based on selection:
- Auto: `auto_sync: true`, `auto_sync_mode: "auto"`
- Notify: `auto_sync: true`, `auto_sync_mode: "notify"`
- Off: `auto_sync: false`, `auto_sync_mode: "off"`

## Step 4: Confirmation

Show:
```
Settings updated!

  Auto-sync: [new value]
```
