---
name: octobercms-backend
description: OctoberCMS backend development - forms, lists, relations, controllers, and admin panel features. Use when working with backend forms (config_form.yaml), lists (config_list.yaml), backend controllers, form widgets, or admin panel customization.
---

# OctoberCMS Backend Development

## MANDATORY: Read Documentation First

**Before answering backend questions, ALWAYS:**

```bash
# 1. Get version
cat .claude/octobercms-config.json

# 2. Read the relevant backend docs
cat .claude/octobercms-docs/${VERSION}.x/plugin/backend/forms.md
cat .claude/octobercms-docs/${VERSION}.x/plugin/backend/lists.md
cat .claude/octobercms-docs/${VERSION}.x/plugin/backend/relations.md
```

**Read the actual docs, don't answer from memory!**

## Key Backend Documentation Files

| Topic | Path |
|-------|------|
| Forms | `plugin/backend/forms.md` |
| Lists | `plugin/backend/lists.md` |
| Relations | `plugin/backend/relations.md` |
| Controllers | `plugin/backend/controllers.md` |
| Widgets | `plugin/backend/widgets.md` |
| Users & Permissions | `plugin/backend/users.md` |

## Backend Form Configuration

Forms are defined in `config_form.yaml`:

```yaml
# models/post/fields.yaml
fields:
    title:
        label: Title
        type: text
        span: full
        
    content:
        label: Content
        type: richeditor
        size: huge
        
tabs:
    fields:
        # Tabbed fields here
        
secondaryTabs:
    fields:
        # Secondary tabbed fields
```

### Field Types by Version

| Field Type | 1.x | 2.x | 3.x | 4.x |
|------------|-----|-----|-----|-----|
| text | ✓ | ✓ | ✓ | ✓ |
| richeditor | ✓ | ✓ | ✓ | ✓ |
| markdown | ✓ | ✓ | ✓ | ✓ |
| codeeditor | ✓ | ✓ | ✓ | ✓ |
| repeater | ✓ | ✓ | ✓ | ✓ |
| nestedform | - | - | ✓ | ✓ |
| sensitive | - | - | ✓ | ✓ |

## Backend List Configuration

Lists are defined in `config_list.yaml`:

```yaml
# models/post/columns.yaml
columns:
    id:
        label: ID
        searchable: true
        sortable: true
        
    title:
        label: Title
        searchable: true
        
    created_at:
        label: Created
        type: datetime
```

## Relations Configuration

Relations use `config_relation.yaml`:

```yaml
# controllers/posts/config_relation.yaml
categories:
    label: Categories
    view:
        list: $/author/plugin/models/category/columns.yaml
    manage:
        form: $/author/plugin/models/category/fields.yaml
        list: $/author/plugin/models/category/columns.yaml
```

## Controller Behaviors

Standard backend controller setup:

```php
class Posts extends Controller
{
    public $implement = [
        \Backend\Behaviors\FormController::class,
        \Backend\Behaviors\ListController::class,
        \Backend\Behaviors\RelationController::class,
    ];
    
    public $formConfig = 'config_form.yaml';
    public $listConfig = 'config_list.yaml';
    public $relationConfig = 'config_relation.yaml';
}
```

## Form Widget Development

Custom form widgets extend `Backend\Classes\FormWidgetBase`:

```php
class MyWidget extends FormWidgetBase
{
    protected $defaultAlias = 'mywidget';
    
    public function render()
    {
        $this->prepareVars();
        return $this->makePartial('mywidget');
    }
    
    protected function prepareVars()
    {
        $this->vars['value'] = $this->getLoadValue();
    }
    
    public function getSaveValue($value)
    {
        return $value;
    }
}
```

## Version-Specific Notes

### 4.x Changes
- New `nestedform` field type for inline related models
- Improved relation handling with pivot data
- Tailor integration for dynamic forms

### 3.x Features
- `sensitive` field type for passwords
- Improved file upload handling
- Better permission granularity

Always consult local documentation for version-specific syntax.
