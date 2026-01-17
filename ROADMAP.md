# OctoberCMS Claude Plugin - Roadmap

## Vision

Enable "auto-edit" mode where Claude can autonomously build complete OctoberCMS projects (e.g., a CRM with clients, projects, tasks) with minimal intervention.

---

## Architecture - Three-Tier Knowledge System

```
Priority 1: Team Rules (explicit, separate plugin)
       ↓
Priority 2: Skills with Workflow Guidance (this plugin)
       ↓
Priority 3: Official Documentation (this plugin)
       ↓
Priority 4: Knowledge Sources - forum + custom URLs (this plugin)
```

---

## This Plugin (Universal)

### 1. Official Documentation ✓ IMPLEMENTED
- Synced from GitHub to `~/.claude/octobercms-docs/` (global, shared across projects)
- All versions (1.x - 4.x) downloaded once, any project can use any version
- Per-project config (`.claude/octobercms-config.json`) stores version selection
- Auto-sync on session start

### 2. Single Core Skill ✓ IMPLEMENTED
One skill with workflow guidance for autonomous development:

- **octobercms-core** - Build order, artisan commands, config file locations, best practices

The skill auto-triggers based on context (OctoberCMS files, directories, mentions). It references documentation for syntax details rather than duplicating content.

### 3. Knowledge Sources (FUTURE)
Extensible knowledge base with user-configurable URLs:

**Config structure:**
```json
{
  "knowledge_sources": [
    {
      "name": "OctoberCMS Forum",
      "url": "https://talk.octobercms.com/api/solutions.json",
      "enabled": true,
      "builtin": true
    },
    {
      "name": "My October Tricks",
      "url": "https://myblog.com/october-tips.json",
      "enabled": true
    }
  ]
}
```

**Commands:**
- `/add-source <url> [name]` - Add custom knowledge source
- `/list-sources` - Show all sources
- `/sync-sources` - Download all enabled sources
- `/remove-source <name>` - Remove a source

---

## Team Plugin (Separate, Optional)

A separate plugin for team-specific preferences that overrides universal patterns.

**Installation:** Can be installed globally (all projects) or per-project.

**Organized by decision domain** (not by docs structure):

```
team-standards/
├── .claude-plugin/
│   └── plugin.json
├── preferences/
│   ├── database.md        # Schema decisions: foreign keys, UUIDs, timestamps, naming
│   ├── models.md          # Model class: traits, $fillable, validation rules
│   ├── controllers.md     # Controller patterns, base classes
│   ├── forms.md           # Form field preferences
│   ├── naming.md          # Naming conventions (tables, columns, classes)
│   └── general.md         # Anything else
└── README.md
```

---

## Phases

### Phase 1: Skills-Based Workflow ✓ COMPLETE
- [x] Enhanced skills with build order and artisan commands
- [x] Skills reference docs for syntax (no duplication)
- [x] Removed patterns folder (overengineered)
- [x] Consolidated 3 skills → 1 skill (`octobercms-core`)
- [x] Removed `generate_index.py` (overengineered)
- [x] Removed `/october` command (skill auto-triggers via context)
- [x] Simplified scripts (`docs_manager.py`, `auto_sync.py`)
- [ ] Test with real scenario (e.g., build a simple plugin)

### Phase 2: Team Preferences Plugin
- [ ] Design separate plugin architecture
- [ ] Create plugin scaffold
- [ ] Implement preferences loading
- [ ] Test override behavior with main plugin

### Phase 3: Knowledge Sources
- [ ] Build forum API endpoint (talk.octobercms.com)
- [ ] Create sync infrastructure for local download
- [ ] Implement custom URL support
- [ ] Add commands: /add-source, /list-sources, /sync-sources, /remove-source
- [ ] Define standard JSON format for sources

---

## Decisions Made

1. **No "Project Awareness"** - Too complex, risk of replicating bad patterns. Keep it simple with explicit rules only.

2. **Forum data stored locally** - Same approach as docs. Sync once, search offline.

3. **Extensible knowledge sources** - Users can add their own URLs (blogs, internal docs, tricks).

4. **Team preferences = separate plugin** - Keeps this plugin universal and shareable across OctoberCMS community.

5. **Skills over patterns** - Workflow guidance embedded in skills is simpler and more maintainable than separate pattern files. Skills reference docs for syntax instead of duplicating content.

6. **Global docs storage** - Docs stored at `~/.claude/octobercms-docs/` (shared across all projects). All versions downloaded once. Per-project config just stores version selection. Avoids duplication, faster setup for new projects. (Future: add fallback to per-project if global permissions fail)

---

## Pending Requests (External)

- [ ] **Developer guidelines in docs repo** - Requested that https://octobercms.com/help/guidelines/developer be added to the official docs repo. (Workaround: guidelines stored locally in `references/developer-guidelines.md`)

---

## Current Status

**Phase:** Phase 1 complete, ready to test

**Last Update:** 2025-01-16 - Major cleanup: consolidated skills, removed overengineered components

**Current Plugin Structure:**
```
octobercms/
├── .claude-plugin/plugin.json
├── commands/
│   ├── setup.md
│   ├── sync-docs.md
│   ├── sync-settings.md
│   └── october-version.md
├── references/
│   └── developer-guidelines.md   ← default coding standards
├── scripts/
│   ├── docs_manager.py
│   └── auto_sync.py
├── skills/
│   └── octobercms-core/SKILL.md
└── hooks/hooks.json
```

**Next Steps:**
1. Test autonomous plugin creation (e.g., "Create a blog plugin with posts and categories")
2. Iterate on skill guidance based on test results
3. Begin Phase 2 planning
