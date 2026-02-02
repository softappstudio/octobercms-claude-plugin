# Changelog

## [1.1.0] - 2026-02-01

### Added
- **Community Answers** - 530+ solved topics from the official OctoberCMS forum, searchable as a knowledge base for troubleshooting
- **CLAUDE.md integration** - Setup now adds OctoberCMS context to `.claude/CLAUDE.md` so the skill auto-triggers without needing to mention "OctoberCMS"
- **Per-project community answers toggle** - `community_answers` setting in config to enable/disable per project
- **Auto-sync for community answers** - Pulls latest community answers on session start alongside docs

### Changed
- Skill now searches both official docs and community answers to find the best solution
- Setup re-run with "No" to reconfigure still updates CLAUDE.md
- Broader skill trigger keywords (plugin, component, partial, tailor, blueprint, etc.)

### Fixed
- Skill not auto-triggering when user doesn't mention "OctoberCMS" explicitly

### Upgrade from 1.0.0
```bash
claude plugin update octobercms@softappstudio
/octobercms:setup
```

## [1.0.0] - 2026-01-19

### Added
- Initial release
- Version auto-detection via `php artisan october:about`
- Global documentation storage at `~/.claude/octobercms-docs/`
- Auto-sync on session start
- Version switching between 1.x, 2.x, 3.x, 4.x
- OctoberCMS core skill with build order, artisan commands, and best practices
- Developer guidelines reference
