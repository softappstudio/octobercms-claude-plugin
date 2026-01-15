---
name: octobercms-frontend
description: OctoberCMS frontend development - CMS pages, components, themes, AJAX framework, and Twig templating. Use when working with theme files (.htm), CMS pages, layouts, partials, components, or frontend AJAX handlers.
---

# OctoberCMS Frontend Development

## MANDATORY: Read Documentation First

**Before answering frontend/CMS questions, ALWAYS:**

```bash
# 1. Get version
cat .claude/octobercms-config.json

# 2. Read the relevant CMS/frontend docs
cat .claude/octobercms-docs/${VERSION}.x/cms/pages.md
cat .claude/octobercms-docs/${VERSION}.x/cms/components.md
cat .claude/octobercms-docs/${VERSION}.x/ajax/handlers.md
```

**Read the actual docs, don't answer from memory!**

## Key Frontend Documentation Files

| Topic | Path |
|-------|------|
| Pages | `cms/pages.md` |
| Layouts | `cms/layouts.md` |
| Partials | `cms/partials.md` |
| Components | `cms/components.md` |
| AJAX Intro | `ajax/introduction.md` |
| AJAX Handlers | `ajax/handlers.md` |
| Themes | `themes/development.md` |

## CMS Page Structure

```twig
title = "Page Title"
url = "/page-url/:param?"
layout = "default"

[componentAlias]
property = "value"
==
<?php
function onStart()
{
    // Page PHP code
}
?>
==
{# Twig markup #}
{% component 'componentAlias' %}
```

## Component Development

Components connect plugins to the frontend:

```php
class MyComponent extends ComponentBase
{
    public function componentDetails()
    {
        return [
            'name' => 'My Component',
            'description' => 'Component description'
        ];
    }
    
    public function defineProperties()
    {
        return [
            'maxItems' => [
                'title' => 'Max Items',
                'type' => 'string',
                'default' => '10',
                'validationPattern' => '^[0-9]+$'
            ]
        ];
    }
    
    public function onRun()
    {
        $this->page['items'] = $this->loadItems();
    }
    
    protected function loadItems()
    {
        return MyModel::take($this->property('maxItems'))->get();
    }
}
```

## AJAX Framework (Version-Specific)

### Version 4.x (Snowboard)

```javascript
// Modern Snowboard syntax
Snowboard.request(this, 'onSubmit', {
    data: { name: 'value' },
    success: (data) => {
        console.log(data.result);
    }
});
```

HTML data attributes:
```html
<button data-request="onSubmit" 
        data-request-data="id: 1"
        data-request-success="handleSuccess(data)">
    Submit
</button>
```

### Version 3.x and Earlier (Storm/jQuery)

```javascript
// jQuery AJAX
$.request('onSubmit', {
    data: { name: 'value' },
    success: function(data) {
        console.log(data.result);
    }
});
```

HTML data attributes:
```html
<button data-request="onSubmit" 
        data-request-data="id: 1">
    Submit
</button>
```

## AJAX Handler Syntax

```php
// In component or page PHP section
function onSubmit()
{
    $name = post('name');
    
    return [
        'result' => 'Success!',
        '#partial-id' => $this->renderPartial('result', ['name' => $name])
    ];
}
```

## Twig Extensions

OctoberCMS adds these Twig features:

### Functions
- `page()` - Access current page
- `partial('name')` - Render partial
- `content('name')` - Render content block
- `component('alias')` - Render component
- `placeholder('name')` - Placeholder content
- `hasPlaceholder('name')` - Check placeholder

### Filters
- `| theme` - Theme asset path
- `| page` - Page URL
- `| trans` - Translation
- `| md` - Markdown to HTML
- `| raw` - Raw output (careful!)

### Tags
```twig
{% styles %}      {# CSS placeholders #}
{% scripts %}     {# JS placeholders #}
{% framework %}   {# Include AJAX framework #}
{% flash %}       {# Flash messages #}
{% placeholder %} {# Define placeholder #}
{% put %}         {# Inject into placeholder #}
```

## Theme Structure

```
themes/
└── mytheme/
    ├── theme.yaml           # Theme config
    ├── pages/               # CMS pages
    ├── layouts/             # Layouts
    ├── partials/            # Partials
    ├── content/             # Content blocks
    ├── assets/              # CSS, JS, images
    │   ├── css/
    │   ├── js/
    │   └── images/
    └── static/              # Static pages plugin
```

## Version-Specific Notes

### 4.x
- Snowboard replaces Storm/jQuery
- Native ES modules support
- Improved asset compilation

### 3.x
- Storm framework (modern jQuery patterns)
- Better Turbo Router support

### 2.x and Earlier
- jQuery-based AJAX
- Older asset pipeline

Always check local docs for exact syntax differences.
