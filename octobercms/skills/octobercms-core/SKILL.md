---
name: octobercms-core
description: OctoberCMS development guidance and best practices. Auto-trigger when the project has a .claude/octobercms-config.json file, or when working with plugins/, themes/, or modules/ directories, or when the user mentions October, OctoberCMS, plugin, component, partial, layout, theme, tailor, blueprint, repeater, richeditor, mediafinder, backend form, backend list, or artisan october.
---

# OctoberCMS Development Skill

## Knowledge Sources

**IMPORTANT: Always search official docs and community answers first when troubleshooting or answering questions. Then explore the project codebase for context.**

Use your judgment on which to search based on the question. For errors and unexpected behavior, community answers are more likely to help. For syntax and API usage, docs are more likely to help. Search both only if the first source doesn't fully answer the question.

### Official Documentation

Version-specific reference for syntax, config formats, and API.

1. Get the project's version:
   ```bash
   cat .claude/octobercms-config.json
   ```

2. Docs are stored globally at `~/.claude/octobercms-docs/`. Explore:
   ```bash
   ls ~/.claude/octobercms-docs/${VERSION}.x/
   ```

3. Search and read relevant files as needed.

If no config exists, tell the user to run `/octobercms:setup` first.

### Community Answers

530+ solved topics from the official OctoberCMS forum. Real-world problems, errors, workarounds, and edge cases.

**Location:** `~/.claude/octobercms-community-answers/`

First check if enabled for this project: read `community_answers` from `.claude/octobercms-config.json`. If `false` or the folder `~/.claude/octobercms-community-answers/` doesn't exist, skip community answers and rely on docs and general knowledge.

Organized by category folders: `need-help/`, `questions/`, `tips-and-tricks/`, `known-issues/`.

**How to search:**

1. Grep for keywords related to the problem across the folder
2. Scan matching filenames — the slugs are descriptive
3. Read the most relevant files (they're small — reading 5-10 is fine)
4. If the first grep is too broad, narrow with more specific terms or combine keywords

**How to use results:**

- **Always attribute the answer:** mention who answered it (the "Answered by" field)
- **Always cite the source:** include the URL from the file metadata
- If multiple topics match, ask follow-up questions to narrow down which applies

If no community answers match, fall back to docs and general knowledge. Not every problem has been asked before.

## Autonomous Development Workflow

When building plugins, follow this **build order**:

1. **Plugin** → Create plugin structure
2. **Models** → Define data structures and relationships
3. **Migrations** → Create database tables
4. **Controllers** → Backend CRUD interfaces
5. **Components** → Frontend integration (if needed)

### Artisan Scaffolding Commands

Common commands (availability varies by version):

```bash
# Create plugin structure
php artisan create:plugin Author.PluginName

# Create model (includes migration)
php artisan create:model Author.PluginName ModelName

# Create controller
php artisan create:controller Author.PluginName ControllerName

# Create component
php artisan create:component Author.PluginName ComponentName

# Create standalone migration
php artisan create:migration Author.PluginName create_tablename_table
```

Other commands may be available: `create:command`, `create:formwidget`, `create:filterwidget`, `create:reportwidget`, `create:job`, `create:seeder`, `create:test`, `create:factory`, `create:contentfield`.

Run `php artisan list create` to see all available scaffolding commands for your version.

### Config Files to Customize

After scaffolding, customize these files:
- `models/modelname/fields.yaml` → Form field definitions
- `models/modelname/columns.yaml` → List column definitions
- `controllers/controllername/config_form.yaml` → Form behavior config
- `controllers/controllername/config_list.yaml` → List behavior config

### Best Practices for Autonomous Work

1. **Use scaffolding** - Run artisan commands to create files, then customize
2. **Follow conventions** - Namespace, file locations, and naming must match OctoberCMS standards
3. **Read docs for syntax** - Config formats vary by version, verify in docs

## Code Conventions

**Default standards:** Follow the official OctoberCMS developer guidelines.

Read the guidelines: `.claude-plugin/octobercms/references/developer-guidelines.md`

These conventions cover:
- Naming (vendors, packages, variables, classes, models, controllers, components)
- Database table and column naming
- PSR exceptions specific to OctoberCMS
- Event naming patterns
- View file naming

**Override behavior:** If a team preferences plugin is installed, team-specific conventions take priority over these defaults.
