#!/usr/bin/env python3
"""
Generate an index of OctoberCMS documentation for quick reference.
This index helps Claude quickly find the right documentation files.
"""

import os
import re
from pathlib import Path

def extract_title(filepath):
    """Extract the first H1 title from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                # Also check for title in frontmatter
                if line.startswith('title:'):
                    return line.split(':', 1)[1].strip().strip('"\'')
        return filepath.stem.replace('-', ' ').title()
    except:
        return filepath.stem.replace('-', ' ').title()


def generate_index(docs_path, version):
    """Generate INDEX.md for the documentation."""
    docs_dir = Path(docs_path) / f"{version}.x"
    
    if not docs_dir.exists():
        print(f"Documentation directory not found: {docs_dir}")
        return None
    
    index_content = f"""# OctoberCMS {version}.x Documentation Index

This index was auto-generated to help navigate the local documentation.

## Quick Reference

**Documentation Path:** `{docs_dir}`

**To read a file:**
```bash
cat {docs_dir}/<path>
```

**To search:**
```bash
grep -r -l -i "search term" {docs_dir}/ --include="*.md"
```

## Documentation Structure

"""
    
    # Organize by directory
    categories = {}
    
    for md_file in sorted(docs_dir.rglob("*.md")):
        rel_path = md_file.relative_to(docs_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
        
        if category not in categories:
            categories[category] = []
        
        title = extract_title(md_file)
        categories[category].append({
            'path': str(rel_path),
            'title': title,
            'filename': md_file.stem
        })
    
    # Category descriptions
    category_descriptions = {
        'setup': 'Installation & Configuration',
        'cms': 'CMS Pages, Layouts, Partials',
        'plugin': 'Plugin Development',
        'backend': 'Backend/Admin Panel',
        'ajax': 'AJAX Framework',
        'database': 'Database & Models',
        'services': 'Services & Helpers',
        'themes': 'Theme Development',
        'console': 'Console Commands',
        'tailor': 'Tailor CMS (4.x)',
        'extend': 'Extending October',
        'root': 'General'
    }
    
    # Write categories
    for category in sorted(categories.keys()):
        files = categories[category]
        desc = category_descriptions.get(category, category.title())
        
        index_content += f"### {desc}\n\n"
        index_content += "| File | Description |\n"
        index_content += "|------|-------------|\n"
        
        for f in files:
            index_content += f"| `{f['path']}` | {f['title']} |\n"
        
        index_content += "\n"
    
    # Common tasks quick reference
    index_content += """## Common Tasks Quick Reference

| Task | Read This File |
|------|---------------|
| Create a plugin | `plugin/registration.md` |
| Backend forms | `plugin/backend/forms.md` |
| Backend lists | `plugin/backend/lists.md` |
| Relations | `plugin/backend/relations.md` |
| Models & DB | `database/model.md` |
| Components | `cms/components.md` |
| AJAX handlers | `ajax/handlers.md` |
| Theme development | `themes/development.md` |

## Search Tips

```bash
# Find all files mentioning "form"
grep -r -l -i "form" """ + str(docs_dir) + """/ --include="*.md"

# Search for specific code patterns
grep -r -n "FormController" """ + str(docs_dir) + """/ --include="*.md"

# Find files in a specific section
ls """ + str(docs_dir) + """/plugin/backend/
```
"""
    
    # Write the index
    index_path = Path(docs_path) / "INDEX.md"
    with open(index_path, 'w') as f:
        f.write(index_content)
    
    print(f"✅ Generated documentation index: {index_path}")
    return index_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: generate_index.py <docs_path> <version>")
        print("Example: generate_index.py .claude/octobercms-docs 4")
        sys.exit(1)
    
    docs_path = sys.argv[1]
    version = sys.argv[2].replace('.x', '')
    
    generate_index(docs_path, version)
