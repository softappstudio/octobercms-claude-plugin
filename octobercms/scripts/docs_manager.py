#!/usr/bin/env python3
"""
OctoberCMS Documentation Manager

Handles cloning, syncing, and checking documentation from GitHub.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_FILE = ".claude/octobercms-config.json"
DOCS_PATH = ".claude/octobercms-docs"
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
    hash_file = Path(DOCS_PATH) / ".git-hash"
    if hash_file.exists():
        return hash_file.read_text().strip()
    return None


def clone_docs(version):
    """Clone documentation for specific version."""
    import shutil
    import tempfile
    
    print(f"📥 Downloading OctoberCMS {version}.x documentation...")
    
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
        docs_path = Path(DOCS_PATH)
        if docs_path.exists():
            shutil.rmtree(docs_path)
        
        # Copy version-specific folder
        docs_path.mkdir(parents=True, exist_ok=True)
        version_src = tmp_path / f"{version}.x"
        version_dst = docs_path / f"{version}.x"
        
        if version_src.exists():
            shutil.copytree(version_src, version_dst)
            # Save commit hash
            (docs_path / ".git-hash").write_text(commit_hash)
            
            # Generate documentation index
            generate_doc_index(DOCS_PATH, version)
            
            return commit_hash
        else:
            print(f"❌ Version {version}.x not found in repository!")
            return None


def generate_doc_index(docs_path, version):
    """Generate INDEX.md for quick documentation reference."""
    docs_dir = Path(docs_path) / f"{version}.x"
    
    if not docs_dir.exists():
        return
    
    print("📑 Generating documentation index...")
    
    index_content = f"""# OctoberCMS {version}.x Documentation Index

## Quick Reference

**Read a file:** `cat {docs_dir}/<path>`
**Search:** `grep -r -l -i "term" {docs_dir}/ --include="*.md"`

## Documentation Files

"""
    
    # List all markdown files organized by directory
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
    
    index_content += """## Common Tasks

| Task | File |
|------|------|
| Plugin basics | `plugin/registration.md` |
| Backend forms | `plugin/backend/forms.md` |
| Backend lists | `plugin/backend/lists.md` |
| Models | `database/model.md` |
| Components | `cms/components.md` |
| AJAX | `ajax/handlers.md` |
"""
    
    index_path = Path(docs_path) / "INDEX.md"
    with open(index_path, 'w') as f:
        f.write(index_content)
    
    print(f"   Index: {index_path}")


def setup(version):
    """Set up OctoberCMS documentation for a specific version."""
    valid_versions = ["1", "2", "3", "4"]
    version = version.replace(".x", "")
    
    if version not in valid_versions:
        print(f"❌ Invalid version: {version}")
        print(f"   Valid versions: {', '.join(v + '.x' for v in valid_versions)}")
        return False
    
    commit_hash = clone_docs(version)
    if not commit_hash:
        return False
    
    # Save configuration
    config = {
        "version": f"{version}.x",
        "docs_path": f"{DOCS_PATH}/{version}.x",
        "last_sync": datetime.utcnow().isoformat() + "Z",
        "commit_hash": commit_hash,
        "repo_url": REPO_URL,
        "branch": BRANCH
    }
    save_config(config)
    
    print(f"\n✅ OctoberCMS {version}.x environment configured!")
    print(f"📁 Documentation: {DOCS_PATH}/{version}.x/")
    print(f"🔗 Commit: {commit_hash[:8]}...")
    print(f"\n💡 Tips:")
    print(f"   • Run /sync-docs to update documentation")
    print(f"   • Run /october help <topic> to search docs")
    
    return True


def sync():
    """Sync documentation with latest from GitHub."""
    config = get_config()
    if not config:
        print("❌ No configuration found. Run /setup first.")
        return False
    
    version = config["version"].replace(".x", "")
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()
    
    if not remote_hash:
        print("❌ Could not fetch remote repository info.")
        return False
    
    print(f"📊 OctoberCMS {config['version']} Documentation Status")
    print(f"   Local:  {local_hash[:8] if local_hash else 'none'}...")
    print(f"   Remote: {remote_hash[:8]}...")
    
    if local_hash == remote_hash:
        print("\n✅ Documentation is up to date!")
        return True
    
    print("\n🔄 Updating documentation...")
    commit_hash = clone_docs(version)
    
    if commit_hash:
        config["last_sync"] = datetime.utcnow().isoformat() + "Z"
        config["commit_hash"] = commit_hash
        save_config(config)
        print(f"\n✅ Documentation updated to {commit_hash[:8]}...")
        return True
    
    return False


def status():
    """Show current configuration status."""
    config = get_config()
    if not config:
        print("❌ No configuration found.")
        print("   Run /setup to configure OctoberCMS version.")
        return
    
    local_hash = get_local_hash()
    remote_hash = get_remote_hash()
    
    print(f"📊 OctoberCMS Configuration Status")
    print(f"")
    print(f"   Version:    {config['version']}")
    print(f"   Docs Path:  {config['docs_path']}")
    print(f"   Last Sync:  {config.get('last_sync', 'unknown')}")
    print(f"   Local Hash: {local_hash[:8] if local_hash else 'none'}...")
    print(f"")
    
    if remote_hash:
        if local_hash == remote_hash:
            print("   Status:     ✅ Up to date")
        else:
            print("   Status:     ⚠️  Updates available")
            print(f"   Remote:     {remote_hash[:8]}...")
    else:
        print("   Status:     ❓ Could not check remote")


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
