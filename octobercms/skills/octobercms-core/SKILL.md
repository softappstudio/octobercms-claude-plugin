---
name: octobercms-core
description: OctoberCMS development guidance and best practices. Use when working with OctoberCMS projects, plugins, themes, or when the user mentions October, OctoberCMS, or is working with files in plugins/, themes/, or modules/ directories typical of OctoberCMS structure.
---

# OctoberCMS Development Skill

## When to Read Documentation

**For questions/explanations:** Answer from knowledge. Reference docs if unsure.

**For code generation:** Read docs for version-specific syntax. Config formats vary between versions.

### How to Read Docs

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
