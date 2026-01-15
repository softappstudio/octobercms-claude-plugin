---
name: octobercms-core
description: OctoberCMS development guidance and best practices. Use when working with OctoberCMS projects, plugins, themes, or when the user mentions October, OctoberCMS, or is working with files in plugins/, themes/, or modules/ directories typical of OctoberCMS structure.
---

# OctoberCMS Development Skill

## MANDATORY: Read Documentation First

**BEFORE answering ANY OctoberCMS question, you MUST:**

1. Read the config to get the version:
   ```bash
   cat .claude/octobercms-config.json
   ```

2. Read the documentation index:
   ```bash
   cat .claude/octobercms-docs/INDEX.md
   ```

3. Search and read relevant documentation files:
   ```bash
   # Search for the topic
   grep -r -l -i "SEARCH_TERM" .claude/octobercms-docs/ --include="*.md" | head -5
   
   # Read the most relevant file
   cat .claude/octobercms-docs/${VERSION}.x/path/to/file.md
   ```

**DO NOT answer from memory. ALWAYS read the local docs first.**

If no config exists, tell the user to run `/setup` first.

## Documentation Structure

After running `/setup`, docs are at `.claude/octobercms-docs/${VERSION}.x/`:

| Topic | File Path |
|-------|-----------|
| Plugin registration | `plugin/registration.md` |
| Backend forms | `plugin/backend/forms.md` |
| Backend lists | `plugin/backend/lists.md` |
| Relations | `plugin/backend/relations.md` |
| Models | `database/model.md` |
| Components | `cms/components.md` |
| AJAX handlers | `ajax/handlers.md` |
| Themes | `themes/development.md` |
| Console commands | `console/commands.md` |
| Pages & layouts | `cms/pages.md`, `cms/layouts.md` |
| Partials | `cms/partials.md` |
| Tailor (4.x only) | `tailor/introduction.md` |

## Workflow

1. **User asks question** → 
2. **Read config** (get version) → 
3. **Search docs** (find relevant files) → 
4. **Read docs** (load content) → 
5. **Answer based on docs** (cite what you read)

## Example

User: "How do I create a backend form?"

You should:
```bash
# 1. Get version
cat .claude/octobercms-config.json
# Shows: version "4.x"

# 2. Read the forms documentation
cat .claude/octobercms-docs/4.x/plugin/backend/forms.md

# 3. Now answer based on what you read
```

## Version Differences (Quick Reference)

Only use this if docs are unavailable:

| Feature | 4.x | 3.x | 2.x | 1.x |
|---------|-----|-----|-----|-----|
| Laravel | 11 | 9 | 6 | 5 |
| PHP | 8.2+ | 8.0+ | 7.4+ | 7.0+ |
| JS Framework | Snowboard | Storm | Storm | jQuery |
| Tailor CMS | ✓ | - | - | - |
| Multisite | ✓ | - | - | - |

## Code Conventions

When generating code, follow OctoberCMS patterns:
- Plugin namespace: `Author\PluginName`
- Use `plugins_path()`, `themes_path()` helpers
- Use behaviors for extensibility
- Always use `Lang::get()` for strings
