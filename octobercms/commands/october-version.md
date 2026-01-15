---
description: Switch OctoberCMS documentation version without full re-setup
argument-hint: <version: 1, 2, 3, or 4>
allowed-tools: Bash, Write, Read
---

# Switch OctoberCMS Version

Quickly switch to a different OctoberCMS documentation version.

## Usage

If $ARGUMENTS is provided, use that version. Otherwise, prompt the user.

## Execution

Run the docs manager script to switch versions:

```bash
python3 .claude-plugins/octobercms/scripts/docs_manager.py setup $VERSION
```

Or if the script isn't available, fall back to manual process:

1. Update `.claude/octobercms-config.json` with new version
2. Remove old documentation: `rm -rf .claude/octobercms-docs`
3. Clone new version documentation

## Post-Switch

After switching:
- Confirm the new version is active
- Note any version-specific behavior changes
- Suggest reviewing migration guides if upgrading/downgrading significantly
