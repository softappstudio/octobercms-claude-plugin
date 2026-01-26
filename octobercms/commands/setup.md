---
description: Initialize OctoberCMS development environment - select version and download documentation
allowed-tools: Bash, Write, Read
---

# OctoberCMS Setup

**CRITICAL INSTRUCTIONS:**
1. Use the EXACT bash commands shown below - do NOT modify them
2. Do NOT add `|| echo "..."` fallbacks to any command
3. Empty output = file/command not found - interpret accordingly
4. Show user-friendly messages based on results, not raw command output

## Step 1: Welcome Banner

Display this banner:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                   ┃
┃   ███████  ██████  ███████ ████████  █████  ██████  ██████        ┃
┃   ██      ██    ██ ██         ██    ██   ██ ██   ██ ██   ██       ┃
┃   ███████ ██    ██ █████      ██    ███████ ██████  ██████        ┃
┃        ██ ██    ██ ██         ██    ██   ██ ██      ██            ┃
┃   ███████  ██████  ██         ██    ██   ██ ██      ██            ┃
┃                        S T U D I O                                ┃
┃                                                                   ┃
┃   OctoberCMS Development Toolkit                                  ┃
┃   https://www.softappstudio.com                                   ┃
┃                                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Step 2: Check Existing Configuration

Check if config exists (do NOT add echo fallbacks):
```bash
test -f .claude/octobercms-config.json && cat .claude/octobercms-config.json || true
```

**If output contains JSON:** Show friendly message:
```
Existing configuration found:
  Version: [version from config]
  Auto-sync: [enabled/disabled]

Would you like to reconfigure? (y/N)
```

**If no config:** Show: `Setting up OctoberCMS development environment...` and proceed.

## Step 3: Auto-Detect Version

Run this exact command (do NOT add echo fallbacks):
```bash
php artisan october:about 2>/dev/null | grep "October CMS Version" || true
```

**If output contains version number** (e.g., "4.0" or "3.6"):
- Extract major version (4.0.0 → 4)
- Show friendly message:
  ```
  Detected OctoberCMS 4.x in this project.

  Use version 4.x? (Y/n)
  ```
- If user confirms (or just presses enter), use detected version
- If user declines, show manual selection

**If output is empty** (no version detected):
- Show: `Could not auto-detect version.` then show manual selection

## Step 4: Manual Version Selection (if needed)

Only show if auto-detection failed or user declined:

```
Which OctoberCMS version is this project using?

  1. 4.x (Latest)
  2. 3.x (Stable)
  3. 2.x (Legacy)
  4. 1.x (Legacy)

Enter choice (1-4):
```

Accept: "1", "2", "3", "4", "4.x", "3.x", etc.

## Step 5: Download Documentation

Check if docs already exist (do NOT add echo fallbacks):
```bash
ls -d ~/.claude/octobercms-docs/${VERSION}.x 2>/dev/null || true
```

**If output shows the path:** Show: `Documentation for ${VERSION}.x already available.`

**If output is empty:**
1. Show: `Downloading OctoberCMS ${VERSION}.x documentation...`
2. Run the download:
```bash
mkdir -p ~/.claude/octobercms-docs && \
git clone --depth 1 --single-branch --branch develop \
  https://github.com/octobercms/docs.git \
  /tmp/octobercms-docs-temp && \
cp -r /tmp/octobercms-docs-temp/${VERSION}.x ~/.claude/octobercms-docs/ && \
git -C /tmp/octobercms-docs-temp rev-parse HEAD > ~/.claude/octobercms-docs/.git-hash && \
rm -rf /tmp/octobercms-docs-temp
```
3. Show: `Documentation downloaded.`

## Step 6: Auto-Sync Preferences

Ask user:
```
Auto-sync documentation updates?

  1. Auto (recommended) - Sync on session start if updates available
  2. Notify - Notify on session start if updates available
  3. Off - Never check automatically
```

Default to "Auto" if user just presses enter.

## Step 7: Save Configuration

```bash
mkdir -p .claude
```

Then write the config file with the collected values:
```json
{
  "version": "${VERSION}.x",
  "last_sync": "${ISO_TIMESTAMP}",
  "auto_sync": true,
  "auto_sync_mode": "auto"
}
```

Adjust `auto_sync` and `auto_sync_mode` based on user choices:
- Auto: `auto_sync: true`, `auto_sync_mode: "auto"`
- Notify: `auto_sync: true`, `auto_sync_mode: "notify"`
- Off: `auto_sync: false`, `auto_sync_mode: "off"`

## Step 8: Confirmation

Show success message:
```
Setup complete!

  Project version: ${VERSION}.x
  Documentation: ~/.claude/octobercms-docs/${VERSION}.x/
  Auto-sync: [Enabled/Notify only/Disabled]

Commands:
  /octobercms:sync-docs       - Manually sync documentation
  /octobercms:october-version - Switch to different version
```
