#!/usr/bin/env python3
"""
OctoberCMS Auto-Sync

Checks for documentation updates on every session start.
Configurable via .claude/octobercms-config.json

Docs are stored GLOBALLY at ~/.claude/octobercms-docs/ (shared across all projects).
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

# Per-project config
CONFIG_FILE = ".claude/octobercms-config.json"

# Global docs location (shared across all projects)
GLOBAL_DOCS_PATH = Path.home() / ".claude" / "octobercms-docs"

REPO_URL = "https://github.com/octobercms/docs.git"
BRANCH = "develop"


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


def do_sync(config):
    """Perform the actual sync operation (only installed versions)."""
    import shutil
    import tempfile

    # Find which versions are currently installed
    installed_versions = []
    if GLOBAL_DOCS_PATH.exists():
        for item in GLOBAL_DOCS_PATH.iterdir():
            if item.is_dir() and item.name.endswith('.x'):
                installed_versions.append(item.name)

    if not installed_versions:
        return False

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
                return False

            # Get commit hash
            result = subprocess.run(
                ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
                capture_output=True, text=True
            )
            commit_hash = result.stdout.strip() if result.returncode == 0 else None

            # Update only installed versions
            for version in installed_versions:
                version_src = tmp_path / version
                version_dst = GLOBAL_DOCS_PATH / version
                if version_src.exists():
                    if version_dst.exists():
                        shutil.rmtree(version_dst)
                    shutil.copytree(version_src, version_dst)

            if commit_hash:
                (GLOBAL_DOCS_PATH / ".git-hash").write_text(commit_hash)

            # Update per-project config
            config["last_sync"] = datetime.utcnow().isoformat() + "Z"
            save_config(config)

            return True

    except (subprocess.TimeoutExpired, Exception):
        return False


def output_message(message):
    """Output a message that will be shown to the user via hook systemMessage."""
    import json as json_module
    print(json_module.dumps({"systemMessage": message}))


def main():
    # Check if we're in an OctoberCMS project
    config = get_config()
    if not config:
        # No config = not set up yet, exit silently
        return

    # Check if auto-sync is enabled
    if not config.get("auto_sync", True):
        return

    # Check for remote updates
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()

    if not remote_hash:
        # Offline - can't check
        return

    if local_hash == remote_hash:
        # Already up to date
        return

    # Updates available
    auto_sync_mode = config.get("auto_sync_mode", "auto")

    if auto_sync_mode == "auto":
        if do_sync(config):
            output_message("OctoberCMS documentation updated.")
    elif auto_sync_mode == "notify":
        output_message("OctoberCMS documentation updates available. Run /octobercms:sync-docs to update.")


if __name__ == "__main__":
    main()
