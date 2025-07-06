# Templates Organization

The templates directory has been reorganized for better structure and maintainability.

## Directory Structure

```
templates/
├── base/                    # Base templates and layout components
│   ├── index.html           # Main base template
│   ├── head.html           # HTML head section
│   └── scripts.html        # JavaScript includes
├── components/              # Reusable UI components
│   ├── banner.html         # Homepage banner
│   ├── footer.html         # Site footer
│   └── navbar.html         # Navigation bar
├── errors/                  # HTTP error pages
│   ├── 400.html            # Bad Request
│   ├── 401.html            # Unauthorized
│   ├── 403.html            # Forbidden
│   ├── 404.html            # Not Found
│   ├── 500.html            # Internal Server Error
│   └── ...                 # Other error codes
├── admin/                   # Django admin customizations
├── homepage/                # Homepage app templates
├── journals/                # Journals app templates
├── noto_garden/            # Noto Garden app templates
└── reference/              # Reference app templates
```

## Template Hierarchy

### Base Templates
- **`base/index.html`**: Main site template that all pages extend
- **`base/head.html`**: HTML head section with meta tags, CSS, and fonts
- **`base/scripts.html`**: JavaScript includes and initialization

### Components
- **`components/banner.html`**: Homepage welcome banner with Japanese text
- **`components/footer.html`**: Site footer with credits and documentation links
- **`components/navbar.html`**: Navigation bar with app links

### Error Pages
All HTTP error pages (400-505) are organized in the `errors/` directory and follow a consistent ninja-themed design.

## Usage

### Extending Base Template
All app templates should extend the base template:
```html
{% extends "base/index.html" %}
```

### Including Components
Include components using the new paths:
```html
{% include "components/banner.html" %}
{% include "components/footer.html" %}
{% include "components/navbar.html" %}
```

### Including Base Elements
Reference base elements:
```html
{% include "base/head.html" %}
{% include "base/scripts.html" %}
```

## Benefits

1. **Clear Separation**: Base, components, and app-specific templates are clearly separated
2. **Reusability**: Components can be easily reused across different templates
3. **Maintainability**: Easier to find and modify specific template types
4. **Scalability**: New apps can follow the same organizational pattern
5. **Error Handling**: All error pages are centralized and consistent

## Migration Notes

All existing templates have been updated to use the new paths. No functional changes were made to the templates themselves, only their organization and references.
