#!/usr/bin/env python3
"""
OctoberCMS Documentation Manager

Handles cloning, syncing, and checking documentation from GitHub.

Docs are stored GLOBALLY at ~/.claude/octobercms-docs/ (shared across all projects).
Config is stored PER-PROJECT at .claude/octobercms-config.json (version selection).
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Per-project config (just stores version selection)
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
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_remote_hash():
    """Get the latest commit hash from remote repository."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", REPO_URL, f"refs/heads/{BRANCH}"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.split()[0] if result.stdout else None
    except subprocess.CalledProcessError:
        return None


def get_local_hash():
    """Get the stored local commit hash."""
    hash_file = GLOBAL_DOCS_PATH / ".git-hash"
    if hash_file.exists():
        return hash_file.read_text().strip()
    return None


def clone_docs():
    """Clone all documentation versions to global location."""
    import shutil
    import tempfile

    print(f"📥 Downloading OctoberCMS documentation (all versions)...")

    # Create temp directory for full clone
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "docs"

        # Clone with depth 1 for efficiency
        subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch",
             "--branch", BRANCH, REPO_URL, str(tmp_path)],
            check=True, capture_output=True
        )

        # Get commit hash
        result = subprocess.run(
            ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True
        )
        commit_hash = result.stdout.strip()

        # Remove old docs
        if GLOBAL_DOCS_PATH.exists():
            shutil.rmtree(GLOBAL_DOCS_PATH)

        # Copy all version folders
        GLOBAL_DOCS_PATH.mkdir(parents=True, exist_ok=True)

        versions_found = []
        for version in ["1", "2", "3", "4"]:
            version_src = tmp_path / f"{version}.x"
            version_dst = GLOBAL_DOCS_PATH / f"{version}.x"
            if version_src.exists():
                shutil.copytree(version_src, version_dst)
                versions_found.append(f"{version}.x")

        # Save commit hash
        (GLOBAL_DOCS_PATH / ".git-hash").write_text(commit_hash)

        print(f"✅ Downloaded versions: {', '.join(versions_found)}")
        print(f"📁 Location: {GLOBAL_DOCS_PATH}")
        return commit_hash


def setup(version):
    """Set up OctoberCMS documentation for a specific version."""
    valid_versions = ["1", "2", "3", "4"]
    version = version.replace(".x", "")

    if version not in valid_versions:
        print(f"❌ Invalid version: {version}")
        print(f"   Valid versions: {', '.join(v + '.x' for v in valid_versions)}")
        return False

    # Check if global docs exist
    version_path = GLOBAL_DOCS_PATH / f"{version}.x"
    commit_hash = get_local_hash()

    if not version_path.exists():
        # Need to download docs
        commit_hash = clone_docs()
        if not commit_hash:
            return False
    else:
        print(f"📚 Using cached documentation")

    # Verify version exists
    if not version_path.exists():
        print(f"❌ Version {version}.x not found in documentation!")
        return False

    # Save per-project configuration
    config = {
        "version": f"{version}.x",
        "last_sync": datetime.utcnow().isoformat() + "Z",
        "auto_sync": True,
        "auto_sync_interval_days": 7
    }
    save_config(config)

    print(f"\n✅ OctoberCMS {version}.x environment configured!")
    print(f"📁 Documentation: {GLOBAL_DOCS_PATH}/{version}.x/")
    if commit_hash:
        print(f"🔗 Commit: {commit_hash[:8]}...")

    return True


def sync():
    """Sync documentation with latest from GitHub."""
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()

    if not remote_hash:
        print("❌ Could not fetch remote repository info.")
        return False

    print(f"📊 OctoberCMS Documentation Status")
    print(f"   Local:  {local_hash[:8] if local_hash else 'none'}...")
    print(f"   Remote: {remote_hash[:8]}...")

    if local_hash == remote_hash:
        print("\n✅ Documentation is up to date!")
        return True

    print("\n🔄 Updating documentation...")
    commit_hash = clone_docs()

    if commit_hash:
        # Update per-project config if exists
        config = get_config()
        if config:
            config["last_sync"] = datetime.utcnow().isoformat() + "Z"
            save_config(config)
        print(f"\n✅ Documentation updated to {commit_hash[:8]}...")
        return True

    return False


def status():
    """Show current configuration status."""
    config = get_config()
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()

    print(f"📊 OctoberCMS Documentation Status")
    print(f"")
    print(f"   Global Docs: {GLOBAL_DOCS_PATH}")

    # List available versions
    available = []
    for v in ["1", "2", "3", "4"]:
        if (GLOBAL_DOCS_PATH / f"{v}.x").exists():
            available.append(f"{v}.x")
    print(f"   Available:   {', '.join(available) if available else 'none (run /setup)'}")

    if config:
        print(f"   Project:     {config['version']}")
    else:
        print(f"   Project:     not configured (run /setup)")

    print(f"   Local Hash:  {local_hash[:8] if local_hash else 'none'}...")
    print(f"")

    if remote_hash:
        if local_hash == remote_hash:
            print("   Status:      ✅ Up to date")
        else:
            print("   Status:      ⚠️  Updates available")
            print(f"   Remote:      {remote_hash[:8]}...")
    else:
        print("   Status:      ❓ Could not check remote")


def main():
    parser = argparse.ArgumentParser(description="OctoberCMS Documentation Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up documentation for a version")
    setup_parser.add_argument("version", help="OctoberCMS version (1, 2, 3, or 4)")
    
    # Sync command
    subparsers.add_parser("sync", help="Sync documentation with latest")
    
    # Status command
    subparsers.add_parser("status", help="Show configuration status")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        sys.exit(0 if setup(args.version) else 1)
    elif args.command == "sync":
        sys.exit(0 if sync() else 1)
    elif args.command == "status":
        status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
