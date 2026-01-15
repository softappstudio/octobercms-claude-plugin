---
description: Sync OctoberCMS documentation with the latest from GitHub
allowed-tools: Bash, Write, Read
---

# Sync OctoberCMS Documentation

Update the local OctoberCMS documentation to the latest version from GitHub.

## Step 1: Read Configuration

```bash
cat .claude/octobercms-config.json
```

If no configuration exists, tell the user to run `/setup` first.

## Step 2: Check for Updates

Fetch the latest commit hash from GitHub and compare with local:

```bash
# Get remote latest commit
REMOTE_HASH=$(git ls-remote https://github.com/octobercms/docs.git refs/heads/develop | cut -f1)
echo "Remote: $REMOTE_HASH"

# Get local sync info
LOCAL_HASH=$(cat .claude/octobercms-docs/.git-hash 2>/dev/null || echo "none")
echo "Local: $LOCAL_HASH"
```

## Step 3: Update if Needed

If hashes differ or user forces update:

```bash
VERSION=$(cat .claude/octobercms-config.json | grep '"version"' | sed 's/.*: "\([0-9]*\).*/\1/')

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
echo "$REMOTE_HASH" > .claude/octobercms-docs/.git-hash

# Update config timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Cleanup
rm -rf /tmp/octobercms-docs-temp
```

## Step 4: Update Configuration

Update the `last_sync` field in `.claude/octobercms-config.json`.

## Step 5: Report Results

Show what was updated:
- Files added/changed (if possible to determine)
- Last sync timestamp
- Documentation version

**Example output:**
```
🔄 OctoberCMS Documentation Sync

Version: 4.x
Status: ✅ Updated to latest
Last sync: 2024-01-15T10:30:00Z
Commit: abc1234...

📝 Tip: Documentation changes since last sync may affect your project.
   Review the changelog at https://octobercms.com/support/articles/release-notes
```
