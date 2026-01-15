---
description: Search and reference OctoberCMS documentation for your configured version
argument-hint: <topic or question>
allowed-tools: Bash, Read, Grep, Glob
---

# OctoberCMS Documentation Helper

Search and retrieve relevant OctoberCMS documentation based on the user's query.

## Prerequisites

First, verify configuration exists:

```bash
cat .claude/octobercms-config.json 2>/dev/null || echo "NO_CONFIG"
```

If no config, prompt user to run `/setup` first.

## Search Strategy

Based on user's query ($ARGUMENTS), search the documentation:

### 1. Identify Relevant Files

Common documentation structure:
- `setup/` - Installation, configuration
- `cms/` - CMS pages, layouts, partials, components
- `plugin/` - Plugin development
- `backend/` - Backend forms, lists, relations
- `ajax/` - AJAX framework
- `database/` - Models, migrations, queries
- `services/` - Laravel services, helpers
- `themes/` - Theme development
- `console/` - Artisan commands

### 2. Search Commands

```bash
# Search for topic in file names
find .claude/octobercms-docs -name "*.md" | grep -i "$TOPIC"

# Search for topic in file contents
grep -r -l -i "$TOPIC" .claude/octobercms-docs/*.x/ --include="*.md"

# Get content from most relevant files
cat .claude/octobercms-docs/${VERSION}.x/relevant-file.md
```

### 3. Response Format

After finding relevant documentation:

1. **Summarize** the key information related to the query
2. **Show code examples** from the docs when available
3. **Link to related topics** the user might want to explore
4. **Note version-specific behavior** if the feature differs across versions

**Example response:**
```
## Backend Forms in OctoberCMS 4.x

Based on the documentation, here's how to create a backend form...

[Relevant code example from docs]

### Related Topics
- Backend Lists: see `plugin/backend/lists.md`
- Form Widgets: see `plugin/backend/widgets.md`

📖 Full documentation: .claude/octobercms-docs/4.x/plugin/backend/forms.md
```
