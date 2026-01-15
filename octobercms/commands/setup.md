---
description: Initialize OctoberCMS development environment - select version and download documentation
allowed-tools: Bash, Write, Read
---

# OctoberCMS Setup

**IMPORTANT: Your response must follow this exact flow:**

1. First, output this banner as plain text:
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
┃   🎃 OctoberCMS Development Toolkit                               ┃
┃   🌐 https://www.softappstudio.com                                ┃
┃                                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

2. Then silently run this check (no announcement):
```bash
cat .claude/octobercms-config.json 2>/dev/null || echo "NO_CONFIG"
```

3. Based on the result:
   - If config exists: Show "Existing configuration found:" with details, then ask if they want to reconfigure
   - If NO_CONFIG: Show "Setting up OctoberCMS development environment..." then proceed directly to version selection

## Step 2: Version Selection

Ask the user which OctoberCMS version they are using. Present these options clearly:

**Which OctoberCMS version are you using?**

1. **4.x** (Latest - recommended for new projects)
2. **3.x** (Stable - most common in production)
3. **2.x** (Legacy)
4. **1.x** (Legacy - limited support)

Wait for user response. Accept formats like "4", "4.x", "3", "3.x", etc.

## Step 3: Clone Documentation

Based on the selected version, clone the appropriate documentation branch:
```bash
# Create docs directory
mkdir -p .claude/octobercms-docs

# Clone the specific version branch (sparse checkout for efficiency)
git clone --depth 1 --single-branch --branch develop \
  https://github.com/octobercms/docs.git \
  /tmp/octobercms-docs-temp

# Copy only the selected version folder
cp -r /tmp/octobercms-docs-temp/${VERSION}.x .claude/octobercms-docs/

# Cleanup
rm -rf /tmp/octobercms-docs-temp
```

Replace `${VERSION}` with the user's selection (4, 3, 2, or 1).

## Step 4: Auto-Sync Preferences (Optional)

Ask the user about automatic documentation updates:

**Would you like documentation to sync automatically?**
- **Auto** (default) - Automatically download updates when available
- **Notify** - Just notify when updates are available
- **Off** - Never check automatically (manual `/sync-docs` only)

**How often should we check for updates?**
- Default: Every 7 days
- Accept: 1-30 days

## Step 5: Save Configuration

Create the configuration file:
```bash
mkdir -p .claude
cat > .claude/octobercms-config.json << 'EOF'
{
  "version": "${VERSION}.x",
  "docs_path": ".claude/octobercms-docs/${VERSION}.x",
  "last_sync": "${TIMESTAMP}",
  "repo_url": "https://github.com/octobercms/docs",
  "branch": "develop",
  "auto_sync": true,
  "auto_sync_mode": "auto",
  "auto_sync_interval_days": 7,
  "auto_sync_silent": false
}
EOF
```

**Configuration options:**
- `auto_sync`: Enable/disable automatic checking (true/false)
- `auto_sync_mode`: "auto" (sync immediately), "notify" (just inform), or "off"
- `auto_sync_interval_days`: Days between update checks (1-30)
- `auto_sync_silent`: If true, only show messages when updates found

## Step 6: Confirmation

Confirm setup completion with:
- Selected version
- Documentation path
- Suggest running `/sync-docs` periodically to keep docs updated
- Suggest trying `/october help [topic]` to search the documentation

**Example output:**
```
✅ OctoberCMS ${VERSION}.x environment configured!

📁 Documentation: .claude/octobercms-docs/${VERSION}.x/
🔄 Auto-sync: Enabled (every 7 days)
❓ Run /october help [topic] to search docs
```