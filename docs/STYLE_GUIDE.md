# Django Style Guide & Naming Conventions

This guide establishes coding standards and naming conventions for the manual Django rebuild project. Following these guidelines will ensure consistency, readability, and adherence to industry best practices.

## Table of Contents

1. [Python & Django Naming Conventions](#python--django-naming-conventions)
2. [File and Directory Structure](#file-and-directory-structure)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Django-Specific Conventions](#django-specific-conventions)
5. [Database Conventions](#database-conventions)
6. [Template and Static Files](#template-and-static-files)
7. [Testing Conventions](#testing-conventions)
8. [Documentation Standards](#documentation-standards)
9. [Development Tools](#development-tools)

## Python & Django Naming Conventions

### General Naming Rules

| Type | Convention | Examples |
|------|------------|----------|
| Variables | `snake_case` | `user_profile`, `total_count` |
| Functions | `snake_case` | `get_user_data()`, `calculate_total()` |
| Classes | `PascalCase` | `UserProfile`, `JournalEntry` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_UPLOAD_SIZE`, `DEFAULT_TIMEOUT` |
| Modules | `snake_case` | `user_auth.py`, `data_utils.py` |
| Packages | `snake_case` | `user_management`, `data_processing` |
| Private attributes | Prefix with underscore | `_internal_method()`, `_private_var` |

### Boolean Variables

Use descriptive prefixes like `is_`, `has_`, `should_`, `can_`:

```python
is_published = models.BooleanField(default=False)
has_comments = models.BooleanField(default=True)
should_notify = True
can_edit = user.has_permission('edit')
```

### Abbreviations

Avoid abbreviations unless they're widely understood:

```python
# Good
user_authentication = True
http_response = requests.get(url)

# Bad
usr_auth = True
resp = requests.get(url)
```

## File and Directory Structure

### Django Project Structure

```
project_name/
├── manage.py
├── project_name/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app_name/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── templates/
    ├── base.html
    └── app_name/
        └── template.html
```

### App Structure (For Larger Apps)

For larger apps, organize by feature or component:

```
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── constants.py       # App-wide constants
├── forms/             # Form classes
│   ├── __init__.py
│   └── user_forms.py
├── management/        # Management commands
│   └── commands/
├── middleware.py      # Custom middleware
├── migrations/
├── models/            # Model classes
│   ├── __init__.py
│   └── user.py
├── serializers/       # DRF serializers
│   ├── __init__.py
│   └── user_serializers.py
├── services/          # Business logic
│   ├── __init__.py
│   └── user_service.py
├── signals.py         # Signal handlers
├── templates/
│   └── app_name/
├── tests/             # Test modules
│   ├── __init__.py
│   ├── test_models.py
│   └── test_views.py
├── urls.py
└── views/             # View classes/functions
    ├── __init__.py
    └── user_views.py
```

## Code Style Guidelines

### PEP 8 Compliance

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specific rules:

- Line length: 88 characters max (Black default)
- Indentation: 4 spaces (no tabs)
- Line breaks: Before binary operators
- Blank lines: 2 between top-level functions/classes, 1 between methods

### Imports

Organize imports in groups with a blank line between each group:

1. Standard library imports
2. Related third-party imports
3. Local application/library-specific imports

```python
# Standard library
import os
import json
from datetime import datetime

# Third-party
import django
from django.db import models
from django.shortcuts import render, redirect

# Local
from .models import User
from .forms import UserForm
from .utils import format_date
```

Use explicit relative imports for intra-package references:

```python
# Good
from .models import User
from ..utils import helper

# Bad
from app_name.models import User
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_total(items, tax_rate=0.1):
    """Calculate total price with tax for a list of items.
    
    Args:
        items (list): A list of dictionaries with 'price' and 'quantity' keys.
        tax_rate (float, optional): The tax rate as a decimal. Defaults to 0.1.
        
    Returns:
        float: The total price including tax.
        
    Raises:
        ValueError: If any item has a negative price or quantity.
    """
```

### Comments

- Use comments sparingly - aim for self-documenting code
- Use comments to explain "why", not "what"
- Update comments when code changes

## Django-Specific Conventions

### URLs

- URL names: `snake_case`
- URL paths: `kebab-case`

```python
# urls.py
urlpatterns = [
    path('journal-entries/', views.journal_list, name='journal_list'),
    path('journal-entries/<int:pk>/', views.journal_detail, name='journal_detail'),
]
```

### Views

- Function-based views: `snake_case`, action-based names
- Class-based views: `PascalCase`, suffixed with `View`

```python
# Function-based
def journal_list(request):
    """Display list of journal entries."""
    
# Class-based
class JournalDetailView(DetailView):
    """Display a single journal entry."""
```

### Forms

- Forms: `PascalCase`, suffixed with `Form`

```python
class JournalEntryForm(forms.ModelForm):
    """Form for creating and editing journal entries."""
```

### Models

- Model classes: `PascalCase`, singular nouns
- Model fields: `snake_case`, descriptive names
- Meta classes: ordered logically

```python
class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    
    class Meta:
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['created_at'])]
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('journal_detail', kwargs={'pk': self.pk})
```

## Database Conventions

### Database Fields

| Field Type | Naming | Example |
|------------|--------|---------|
| Primary Keys | `id` | `id = models.AutoField(primary_key=True)` |
| Foreign Keys | `<model>_id` | `journal_id = models.ForeignKey(Journal)` |
| Created timestamps | `created_at` | `created_at = models.DateTimeField(auto_now_add=True)` |
| Updated timestamps | `updated_at` | `updated_at = models.DateTimeField(auto_now=True)` |
| Boolean flags | `is_*`, `has_*` | `is_active = models.BooleanField(default=True)` |

### Database Table Names

- Table names: `<app_name>_<model_name>` (lowercase)
- Many-to-many tables: `<model1>_<model2>` (alphabetical order)

## Template and Static Files

### Templates

- Template files: `snake_case.html`
- Template directories: Match app names and structure

```
templates/
├── base.html
└── journals/
    ├── journal_list.html
    └── journal_detail.html
```

### CSS Classes

Use [BEM methodology](http://getbem.com/) (Block, Element, Modifier) for CSS:

```html
<!-- Block component -->
<div class="journal-card">
    <!-- Element that depends on the block -->
    <h2 class="journal-card__title">Title</h2>
    <!-- Element with modifier -->
    <div class="journal-card__content journal-card__content--featured">
        Content here
    </div>
</div>
```

### Static Files

- JavaScript files: `kebab-case.js`
- CSS files: `kebab-case.css`
- Image files: `kebab-case.jpg/png/etc`

```
static/
├── css/
│   ├── base.css
│   └── journal-styles.css
├── js/
│   ├── main.js
│   └── journal-features.js
└── images/
    ├── logo.png
    └── user-avatar.jpg
```

## Testing Conventions

### Test Files and Classes

- Test files: Prefix with `test_`
- Test classes: Suffix with `Test`
- Test methods: Prefix with `test_`

```python
# test_models.py
class JournalEntryTest(TestCase):
    def test_creation_with_valid_data(self):
        """Test creating a journal with valid data."""
        
    def test_str_method_returns_title(self):
        """Test __str__ method returns the journal title."""
```

### Test Organization

Group tests by:
1. Model tests
2. View tests
3. Form tests
4. API tests
5. Integration tests

## Documentation Standards

### Project README

Each project should have a README.md with:

1. Project description
2. Setup instructions
3. Usage examples
4. Development guidelines
5. Deployment notes
6. License information

### App README

Each app should have a README.md with:

1. App purpose
2. Key models and views
3. Business logic overview
4. Special considerations

### Change Log

Keep a `CHANGELOG.md` file following [Keep a Changelog](https://keepachangelog.com/) format.

## Development Tools

### Recommended Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style guide enforcement
- **pylint**: Code analysis
- **pytest**: Testing framework

### VSCode Settings

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "isort.args": ["--profile", "black"],
    "python.testing.pytestEnabled": true
}
```

### Pre-commit Setup

Use [pre-commit](https://pre-commit.com/) to enforce these standards:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-json
-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
```

## Quick Reference Checklist

### Naming
- [ ] Variables and functions use `snake_case`
- [ ] Classes use `PascalCase`
- [ ] Constants use `UPPER_SNAKE_CASE`
- [ ] Boolean variables use `is_`, `has_` prefixes
- [ ] Files use appropriate naming conventions

### Code Style
- [ ] Indentation is 4 spaces
- [ ] Line length <= 88 characters
- [ ] Imports are grouped properly
- [ ] Docstrings follow Google style
- [ ] Comments explain "why", not "what"

### Django
- [ ] URLs follow naming conventions
- [ ] Models follow best practices
- [ ] Templates follow naming patterns
- [ ] Static files are organized properly

### Testing
- [ ] Tests are organized by type
- [ ] Test methods are descriptive
- [ ] Each feature has test coverage

---

## Resources

- [Django Documentation Style Guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Django Best Practices](https://django-best-practices.readthedocs.io/en/latest/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
