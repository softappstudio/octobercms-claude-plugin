---
description: Switch OctoberCMS documentation version without full re-setup
argument-hint: <version: 1, 2, 3, or 4>
allowed-tools: Bash, Write, Read
---

# Switch OctoberCMS Version

Quickly switch to a different OctoberCMS documentation version.

## Step 1: Get Target Version

If $ARGUMENTS is provided, use that version. Otherwise, ask the user which version they want:
- **4.x** (Latest)
- **3.x** (Stable)
- **2.x** (Legacy)
- **1.x** (Legacy)

## Step 2: Download New Documentation

```bash
VERSION=<selected version number>

# Remove old docs
rm -rf .claude/octobercms-docs

# Clone fresh
git clone --depth 1 --single-branch --branch develop \
  https://github.com/octobercms/docs.git \
  /tmp/octobercms-docs-temp

# Copy selected version
mkdir -p .claude/octobercms-docs
cp -r /tmp/octobercms-docs-temp/${VERSION}.x .claude/octobercms-docs/

# Save commit hash
git -C /tmp/octobercms-docs-temp rev-parse HEAD > .claude/octobercms-docs/.git-hash

# Cleanup
rm -rf /tmp/octobercms-docs-temp
```

## Step 3: Update Configuration

Update `.claude/octobercms-config.json` with:
- New version
- Updated last_sync timestamp
- New commit hash

## Step 4: Confirm

```
✅ Switched to OctoberCMS ${VERSION}.x

📁 Documentation: .claude/octobercms-docs/${VERSION}.x/
```
