---
description: Switch OctoberCMS documentation version without full re-setup
argument-hint: <version: 1, 2, 3, or 4>
allowed-tools: Bash, Write, Read, Edit
---

# Switch OctoberCMS Version

**CRITICAL INSTRUCTIONS:**
1. Run ALL bash commands silently - do NOT show command output to user
2. Do NOT add `|| echo "..."` fallbacks to any command
3. Do NOT ask for permission to update the config file - just do it
4. Only show the user-friendly messages specified in each step

## Step 1: Get Target Version

**If $ARGUMENTS provided:** Use that version (accept "4", "4.x", "3", "3.x", etc.)

**If no arguments:** Ask user:
```
Switch to which OctoberCMS version?

  1. 4.x (Latest)
  2. 3.x (Stable)
  3. 2.x (Legacy)
  4. 1.x (Legacy)

Enter choice (1-4):
```

## Step 2: Check Current Configuration

Check if config exists (do NOT add echo fallbacks):
```bash
test -f .claude/octobercms-config.json && cat .claude/octobercms-config.json || true
```

**If output is empty:** Show: `No OctoberCMS configuration found. Run /octobercms:setup first.` and stop.

**If output contains JSON:** Check if already on requested version. If same version, show: `Already using version ${VERSION}.x` and stop.

## Step 3: Check if Version Exists Globally

Check if docs exist (do NOT add echo fallbacks):
```bash
ls -d ~/.claude/octobercms-docs/${VERSION}.x 2>/dev/null || true
```

**If output shows the path:** Show: `Switching to ${VERSION}.x...`

**If output is empty:**
1. Show: `Version ${VERSION}.x not downloaded yet. Downloading...`
2. Run:
```bash
mkdir -p ~/.claude/octobercms-docs && \
git clone --depth 1 --single-branch --branch develop \
  https://github.com/octobercms/docs.git \
  /tmp/octobercms-docs-temp && \
cp -r /tmp/octobercms-docs-temp/${VERSION}.x ~/.claude/octobercms-docs/ && \
rm -rf /tmp/octobercms-docs-temp
```
3. Show: `Downloaded.`

## Step 4: Update Configuration

Update the `version` field in `.claude/octobercms-config.json` to `${VERSION}.x`.

## Step 5: Confirmation

Show success:
```
Switched to OctoberCMS ${VERSION}.x

  Documentation: ~/.claude/octobercms-docs/${VERSION}.x/
```
