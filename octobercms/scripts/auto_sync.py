#!/usr/bin/env python3
"""
OctoberCMS Auto-Sync

Automatically checks for documentation updates on session start.
Configurable via .claude/octobercms-config.json
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_FILE = ".claude/octobercms-config.json"
DOCS_PATH = ".claude/octobercms-docs"
REPO_URL = "https://github.com/octobercms/docs.git"
BRANCH = "develop"

# Default settings
DEFAULT_AUTO_SYNC = True
DEFAULT_SYNC_INTERVAL_DAYS = 7
DEFAULT_SILENT_MODE = False  # If True, only show output when updates found


def get_config():
    """Load existing configuration."""
    config_path = Path(CONFIG_FILE)
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return None


def save_config(config):
    """Save configuration to file."""
    config_path = Path(CONFIG_FILE)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_remote_hash():
    """Get the latest commit hash from remote repository."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", REPO_URL, f"refs/heads/{BRANCH}"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.split()[0]
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return None


def get_local_hash():
    """Get the stored local commit hash."""
    hash_file = Path(DOCS_PATH) / ".git-hash"
    if hash_file.exists():
        return hash_file.read_text().strip()
    return None


def should_check_updates(config):
    """Determine if we should check for updates based on last sync time."""
    last_sync = config.get("last_sync")
    if not last_sync:
        return True
    
    try:
        last_sync_date = datetime.fromisoformat(last_sync.replace("Z", "+00:00"))
        interval_days = config.get("auto_sync_interval_days", DEFAULT_SYNC_INTERVAL_DAYS)
        threshold = datetime.now(last_sync_date.tzinfo) - timedelta(days=interval_days)
        return last_sync_date < threshold
    except (ValueError, TypeError):
        return True


def do_sync(config):
    """Perform the actual sync operation."""
    import shutil
    import tempfile
    
    version = config["version"].replace(".x", "")
    
    print(f"📥 Syncing OctoberCMS {version}.x documentation...")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "docs"
            
            # Clone with depth 1
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "--single-branch",
                 "--branch", BRANCH, REPO_URL, str(tmp_path)],
                capture_output=True, timeout=60
            )
            
            if result.returncode != 0:
                print("⚠️  Could not fetch documentation updates")
                return False
            
            # Get commit hash
            result = subprocess.run(
                ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
                capture_output=True, text=True
            )
            commit_hash = result.stdout.strip() if result.returncode == 0 else None
            
            # Remove old docs and copy new
            docs_path = Path(DOCS_PATH)
            if docs_path.exists():
                shutil.rmtree(docs_path)
            
            docs_path.mkdir(parents=True, exist_ok=True)
            version_src = tmp_path / f"{version}.x"
            version_dst = docs_path / f"{version}.x"
            
            if version_src.exists():
                shutil.copytree(version_src, version_dst)
                if commit_hash:
                    (docs_path / ".git-hash").write_text(commit_hash)
                
                # Generate documentation index
                generate_doc_index(docs_path, version)
                
                # Update config
                config["last_sync"] = datetime.utcnow().isoformat() + "Z"
                config["commit_hash"] = commit_hash
                save_config(config)
                
                print(f"✅ Documentation updated ({commit_hash[:8]}...)")
                return True
            else:
                print(f"⚠️  Version {version}.x not found")
                return False
                
    except subprocess.TimeoutExpired:
        print("⚠️  Sync timed out")
        return False
    except Exception as e:
        print(f"⚠️  Sync error: {e}")
        return False


def generate_doc_index(docs_path, version):
    """Generate INDEX.md for quick documentation reference."""
    docs_dir = docs_path / f"{version}.x"
    
    if not docs_dir.exists():
        return
    
    index_content = f"""# OctoberCMS {version}.x Documentation Index

**Read:** `cat {docs_dir}/<path>`
**Search:** `grep -r -l -i "term" {docs_dir}/ --include="*.md"`

## Files

"""
    
    categories = {}
    for md_file in sorted(docs_dir.rglob("*.md")):
        rel_path = md_file.relative_to(docs_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "general"
        if category not in categories:
            categories[category] = []
        categories[category].append(str(rel_path))
    
    for category in sorted(categories.keys()):
        index_content += f"### {category.title()}\n"
        for filepath in categories[category]:
            index_content += f"- `{filepath}`\n"
        index_content += "\n"
    
    index_path = docs_path / "INDEX.md"
    with open(index_path, 'w') as f:
        f.write(index_content)


def main():
    # Check if we're in an OctoberCMS project
    config = get_config()
    if not config:
        # No config = not set up yet, exit silently
        return
    
    # Check if auto-sync is enabled
    auto_sync_enabled = config.get("auto_sync", DEFAULT_AUTO_SYNC)
    if not auto_sync_enabled:
        return
    
    silent_mode = config.get("auto_sync_silent", DEFAULT_SILENT_MODE)
    
    # Check if enough time has passed since last sync
    if not should_check_updates(config):
        if not silent_mode:
            print(f"📚 OctoberCMS {config['version']} docs loaded")
        return
    
    # Check for remote updates
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()
    
    if not remote_hash:
        if not silent_mode:
            print(f"📚 OctoberCMS {config['version']} docs loaded (offline)")
        return
    
    if local_hash == remote_hash:
        # Update last_sync even if no changes, so we don't check every session
        config["last_sync"] = datetime.utcnow().isoformat() + "Z"
        save_config(config)
        if not silent_mode:
            print(f"📚 OctoberCMS {config['version']} docs up to date")
        return
    
    # Updates available!
    print(f"🔄 OctoberCMS documentation updates available")
    
    # Check if auto-sync or just notify
    auto_sync_mode = config.get("auto_sync_mode", "auto")  # "auto", "notify", "ask"
    
    if auto_sync_mode == "auto":
        do_sync(config)
    elif auto_sync_mode == "notify":
        print(f"   Run /sync-docs to update")
    # "ask" mode would require interactive input, not suitable for hooks


if __name__ == "__main__":
    main()
