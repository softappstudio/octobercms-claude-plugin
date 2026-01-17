#!/usr/bin/env python3
"""
OctoberCMS Auto-Sync

Automatically checks for documentation updates on session start.
Configurable via .claude/octobercms-config.json

Docs are stored GLOBALLY at ~/.claude/octobercms-docs/ (shared across all projects).
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Per-project config
CONFIG_FILE = ".claude/octobercms-config.json"

# Global docs location (shared across all projects)
GLOBAL_DOCS_PATH = Path.home() / ".claude" / "octobercms-docs"

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
    hash_file = GLOBAL_DOCS_PATH / ".git-hash"
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
    """Perform the actual sync operation (all versions globally)."""
    import shutil
    import tempfile

    print(f"📥 Syncing OctoberCMS documentation (all versions)...")

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

            # Remove old docs and copy all versions
            if GLOBAL_DOCS_PATH.exists():
                shutil.rmtree(GLOBAL_DOCS_PATH)

            GLOBAL_DOCS_PATH.mkdir(parents=True, exist_ok=True)

            for version in ["1", "2", "3", "4"]:
                version_src = tmp_path / f"{version}.x"
                version_dst = GLOBAL_DOCS_PATH / f"{version}.x"
                if version_src.exists():
                    shutil.copytree(version_src, version_dst)

            if commit_hash:
                (GLOBAL_DOCS_PATH / ".git-hash").write_text(commit_hash)

            # Update per-project config
            config["last_sync"] = datetime.utcnow().isoformat() + "Z"
            save_config(config)

            print(f"✅ Documentation updated ({commit_hash[:8]}...)")
            print(f"📁 Location: {GLOBAL_DOCS_PATH}")
            return True

    except subprocess.TimeoutExpired:
        print("⚠️  Sync timed out")
        return False
    except Exception as e:
        print(f"⚠️  Sync error: {e}")
        return False


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
