---
description: Sync OctoberCMS documentation with the latest from GitHub
allowed-tools: Bash, Write, Read, Edit
---

# Sync OctoberCMS Documentation

**CRITICAL INSTRUCTIONS:**
1. Run ALL bash commands silently - do NOT show command output to user
2. Do NOT add `|| echo "..."` fallbacks to any command
3. Do NOT ask for permission to update the config file - just do it
4. Only show the user-friendly messages specified below

## Step 1: Check Configuration

Run silently:
```bash
test -f .claude/octobercms-config.json && cat .claude/octobercms-config.json || true
```

**If output is empty:** Show: `No OctoberCMS configuration found. Run /octobercms:setup first.` and stop.

**If output contains JSON:** Extract the version and continue.

## Step 2: Check for Updates

Show: `Checking for documentation updates...`

Run silently and store results (do NOT show output):
```bash
git ls-remote https://github.com/octobercms/docs.git refs/heads/develop | cut -f1
```
```bash
cat ~/.claude/octobercms-docs/.git-hash 2>/dev/null || true
```

**If hashes are equal:** Show: `Documentation is already up to date.` and stop.

**If different:** Continue.

## Step 3: Update Documentation

Show: `Downloading updates...`

Run ALL these commands silently (do NOT show output to user):
```bash
# Get installed versions
ls -d ~/.claude/octobercms-docs/*.x 2>/dev/null | xargs -n1 basename || true

# Clone repo
git clone --depth 1 --single-branch --branch develop \
  https://github.com/octobercms/docs.git \
  /tmp/octobercms-docs-temp

# For each installed version (e.g., 4.x):
rm -rf ~/.claude/octobercms-docs/4.x
cp -r /tmp/octobercms-docs-temp/4.x ~/.claude/octobercms-docs/

# Save hash
git -C /tmp/octobercms-docs-temp rev-parse HEAD > ~/.claude/octobercms-docs/.git-hash

# Cleanup
rm -rf /tmp/octobercms-docs-temp
```

## Step 4: Update Configuration

Update `last_sync` in `.claude/octobercms-config.json` to current ISO timestamp.
**Do NOT ask for permission - just update the file.**

## Step 5: Confirmation

Show ONLY this message:
```
Documentation updated!

  Project version: [version]
  Synced versions: [versions, e.g., "4.x"]
  Location: ~/.claude/octobercms-docs/
```
