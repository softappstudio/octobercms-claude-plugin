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
5. Execute ALL steps in order (1-10). Do NOT skip any step.

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

**If output contains JSON:** Show friendly message and ask:
```
Existing configuration found:
  Version: [version from config]
  Auto-sync: [enabled/disabled]

Would you like to reconfigure?

  1. Yes - Go through full setup again
  2. No - Keep current settings
```

**Present Yes as the first option.**

If user says **No**: skip Steps 3-7 (version, docs download, community answers, auto-sync) but **still run Step 8** (CLAUDE.md update). Then show `Configuration unchanged.` and stop.

**If no config:** Show: `Setting up OctoberCMS development environment...` and proceed through all steps.

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

## Step 7: Download Community Answers

Ask the user:
```
Install community answers knowledge base?
530+ solved topics from the official OctoberCMS forum to help troubleshoot issues.

  1. Yes (recommended)
  2. No

Enter choice (1-2):
```

Default to "Yes" if user just presses enter.

**If Yes:**

Check if already exists (do NOT add echo fallbacks):
```bash
ls -d ~/.claude/octobercms-community-answers 2>/dev/null || true
```

If output shows the path: Show: `Community answers already available.`

If output is empty:
1. Show: `Downloading community answers...`
2. Run:
```bash
git clone --depth 1 \
  https://github.com/softappstudio/octobercms-community-answers.git \
  ~/.claude/octobercms-community-answers
```
3. Show: `Community answers downloaded.`

**If No:** Show: `Skipped community answers.` and continue. Save this choice in config (see Step 9).

## Step 8: Update CLAUDE.md

Check if `.claude/CLAUDE.md` exists and read it.

- **If it contains "octobercms-core":** Check if the version matches. If it says a different version than `${VERSION}.x`, replace that line with the correct version. Do NOT append a duplicate block.
- **If it exists but does NOT contain "octobercms-core":** Append the following block to the end (do NOT overwrite existing content).
- **If it does not exist:** Create it with **only** the block below.

```markdown

# OctoberCMS Project

This is an OctoberCMS ${VERSION}.x project. Always use the octobercms-core skill for any development questions, errors, or code generation.
```

**Do NOT ask for permission — just do it. Do NOT add any extra text, disclaimers, or comments. Write EXACTLY the block above, nothing more.**

## Step 9: Save Configuration

```bash
mkdir -p .claude
```

Then write the config file with the collected values:
```json
{
  "version": "${VERSION}.x",
  "last_sync": "${ISO_TIMESTAMP}",
  "auto_sync": true,
  "auto_sync_mode": "auto",
  "community_answers": true
}
```

Adjust values based on user choices:
- Auto-sync Auto: `auto_sync: true`, `auto_sync_mode: "auto"`
- Auto-sync Notify: `auto_sync: true`, `auto_sync_mode: "notify"`
- Auto-sync Off: `auto_sync: false`, `auto_sync_mode: "off"`
- Community answers Yes: `community_answers: true`
- Community answers No: `community_answers: false`

## Step 10: Confirmation

Show success message:
```
Setup complete!

  Project version: ${VERSION}.x
  Documentation: ~/.claude/octobercms-docs/${VERSION}.x/
  Community answers: [Installed/Not installed]
  Auto-sync: [Enabled/Notify only/Disabled]

Commands:
  /octobercms:sync-docs       - Manually sync documentation
  /octobercms:october-version - Switch to different version
```
