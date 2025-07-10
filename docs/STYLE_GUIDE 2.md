# Django Style Guide & Naming Conventions

A comprehensive guide to industry-standard naming conventions, coding style, and best practices for Django development.

## Table of Contents

1. [Python & Django Naming Conventions](#python--django-naming-conventions)
2. [File and Directory Structure](#file-and-directory-structure)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Django-Specific Conventions](#django-specific-conventions)
5. [Database Conventions](#database-conventions)
6. [Template and Static Files](#template-and-static-files)
7. [Testing Conventions](#testing-conventions)
8. [Documentation Standards](#documentation-standards)

## Python & Django Naming Conventions

### Variables and Functions
```python
# Use snake_case for variables and functions
user_profile = UserProfile.objects.get(id=1)
total_count = 0
is_active = True

def calculate_total_price(items):
    """Calculate the total price of items."""
    return sum(item.price for item in items)

def get_user_by_email(email):
    """Retrieve user by email address."""
    return User.objects.filter(email=email).first()
```

### Classes
```python
# Use PascalCase for class names
class UserProfile(models.Model):
    pass

class JournalEntry(models.Model):
    pass

class NotificationService:
    pass

class EmailValidatorMixin:
    pass
```

### Constants
```python
# Use UPPER_SNAKE_CASE for constants
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
DEFAULT_LANGUAGE = 'en'
CACHE_TIMEOUT = 300
API_VERSION = 'v1'

# In settings.py
DEBUG = False
SECRET_KEY = 'your-secret-key'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### Django Models
```python
class Journal(models.Model):
    # Field names: snake_case
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    # Meta class
    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
        ordering = ['-created_at']
        
    # Methods: snake_case
    def get_absolute_url(self):
        return reverse('journals:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title
```

## File and Directory Structure

### Project Structure
```
project_name/
├── project_name/           # Main project directory (snake_case)
│   ├── __init__.py
│   ├── settings/          # Settings module
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                  # All Django apps
│   ├── __init__.py
│   ├── homepage/          # App names: snake_case
│   ├── journal_entries/   # Use descriptive names
│   ├── user_profiles/
│   └── note_garden/
├── static/
├── templates/
├── media/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── docs/
├── scripts/
└── tests/
```

### App Structure
```
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py              # If needed
├── managers.py           # Custom managers
├── migrations/
├── models.py
├── serializers.py        # For DRF
├── signals.py            # If using signals
├── templatetags/         # Custom template tags
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_forms.py
├── urls.py
├── utils.py              # Utility functions
└── views.py
```

### File Naming
```python
# Python files: snake_case
user_profile.py
email_utils.py
custom_validators.py

# Template files: snake_case
user_profile.html
email_template.html
base_layout.html

# Static files: kebab-case or snake_case
main-style.css
user-profile.js
bootstrap.min.css
```

## Code Style Guidelines

### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime, timedelta

# Third-party imports
import requests
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Local application imports
from .models import Journal
from .forms import JournalForm
from apps.homepage.models import VisitorTracking
```

### Line Length and Formatting
```python
# Keep lines under 88 characters (Black formatter standard)
# Use implicit line continuation inside parentheses
def create_journal_entry(
    title,
    content,
    author,
    tags=None,
    is_published=False
):
    """Create a new journal entry with validation."""
    if not title or not content:
        raise ValueError("Title and content are required")
    
    return Journal.objects.create(
        title=title,
        content=content,
        author=author,
        is_published=is_published
    )

# Long queries
journals = Journal.objects.filter(
    is_published=True,
    created_at__gte=start_date
).select_related(
    'author'
).prefetch_related(
    'tags'
).order_by('-created_at')
```

### Docstrings
```python
def calculate_reading_time(content):
    """
    Calculate estimated reading time for content.
    
    Args:
        content (str): The text content to analyze
        
    Returns:
        int: Estimated reading time in minutes
        
    Raises:
        ValueError: If content is empty or None
    """
    if not content:
        raise ValueError("Content cannot be empty")
    
    words = len(content.split())
    return max(1, words // 200)  # Average 200 words per minute
```

## Django-Specific Conventions

### Views
```python
# Function-based views: snake_case
def journal_list(request):
    """Display list of published journals."""
    pass

def journal_detail(request, pk):
    """Display journal detail page."""
    pass

# Class-based views: PascalCase
class JournalListView(ListView):
    model = Journal
    template_name = 'journals/list.html'
    context_object_name = 'journals'

class JournalCreateView(CreateView):
    model = Journal
    form_class = JournalForm
    template_name = 'journals/create.html'
```

### URLs
```python
# URL patterns: kebab-case
urlpatterns = [
    path('', views.journal_list, name='journal-list'),
    path('<int:pk>/', views.journal_detail, name='journal-detail'),
    path('create/', views.journal_create, name='journal-create'),
    path('<int:pk>/edit/', views.journal_edit, name='journal-edit'),
    path('<int:pk>/delete/', views.journal_delete, name='journal-delete'),
    
    # Namespaced URLs
    path('api/v1/', include('api.urls', namespace='api-v1')),
]

# URL names: kebab-case with namespace
# Usage: reverse('journals:journal-detail', kwargs={'pk': 1})
```

### Forms
```python
class JournalForm(forms.ModelForm):
    """Form for creating and editing journal entries."""
    
    class Meta:
        model = Journal
        fields = ['title', 'content', 'tags', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def clean_title(self):
        """Validate title field."""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long")
        return title
```

## Database Conventions

### Model Fields
```python
class Journal(models.Model):
    # Primary key (Django creates automatically)
    # id = models.AutoField(primary_key=True)
    
    # Use descriptive field names
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)
    
    # Foreign keys: end with object name
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    
    # Many-to-many: plural
    tags = models.ManyToManyField('Tag', blank=True)
    
    # Boolean fields: use is_, has_, can_, etc.
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    has_comments = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Counts and metrics
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
```

### Database Table Names
```python
class Journal(models.Model):
    class Meta:
        # Django creates: appname_journal
        db_table = 'journals_journal'  # Only if needed to override
        
class UserProfile(models.Model):
    class Meta:
        # Django creates: appname_userprofile
        pass  # Use default naming
```

## Template and Static Files

### Template Naming
```html
<!-- Base templates -->
base.html
base_admin.html

<!-- App templates: app_name/template_name.html -->
journals/journal_list.html
journals/journal_detail.html
journals/journal_form.html

<!-- Partial templates: start with underscore -->
journals/_journal_card.html
components/_navbar.html
includes/_pagination.html
```

### Template Structure
```html
<!-- journals/journal_detail.html -->
{% extends "base.html" %}
{% load static %}
{% load journal_extras %}

{% block title %}{{ journal.title }} - Journals{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/journals.css' %}">
{% endblock %}

{% block content %}
    <article class="journal-detail">
        <h1 class="journal-title">{{ journal.title }}</h1>
        <div class="journal-meta">
            <time datetime="{{ journal.created_at|date:'c' }}">
                {{ journal.created_at|date:'F j, Y' }}
            </time>
        </div>
        <div class="journal-content">
            {{ journal.content|markdown }}
        </div>
    </article>
{% endblock %}

{% block extra_js %}
    <script src="{% static 'js/journals.js' %}"></script>
{% endblock %}
```

### CSS Class Naming (BEM Methodology)
```css
/* Block__Element--Modifier */
.journal-card { }
.journal-card__title { }
.journal-card__content { }
.journal-card__meta { }
.journal-card--featured { }
.journal-card--draft { }

/* Layout classes */
.container { }
.row { }
.col { }

/* Utility classes */
.text-center { }
.mb-3 { }
.d-none { }
```

## Testing Conventions

### Test File Structure
```python
# tests/test_models.py
class JournalModelTest(TestCase):
    """Test cases for Journal model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_journal_creation(self):
        """Test creating a journal entry."""
        journal = Journal.objects.create(
            title='Test Journal',
            content='Test content',
            author=self.user
        )
        self.assertEqual(journal.title, 'Test Journal')
        self.assertFalse(journal.is_published)
    
    def test_journal_str_representation(self):
        """Test journal string representation."""
        journal = Journal(title='Test Journal')
        self.assertEqual(str(journal), 'Test Journal')
```

### Test Method Naming
```python
# Pattern: test_[what_is_being_tested]
def test_journal_creation(self):
def test_invalid_email_validation(self):
def test_user_can_edit_own_journal(self):
def test_anonymous_user_cannot_create_journal(self):
def test_journal_list_shows_published_only(self):
```

## Documentation Standards

### README Structure
```markdown
# Project Name

Brief description of the project.

## Features

- Feature 1
- Feature 2

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
```

## Usage

How to use the project.

## Contributing

Guidelines for contributing.

## License

License information.
```

### Changelog Format
```markdown
# Changelog

## [1.2.0] - 2025-01-15

### Added
- New journal search functionality
- User profile avatars

### Changed
- Improved journal list performance
- Updated admin interface

### Fixed
- Fixed pagination bug in journal list
- Corrected timezone handling

### Removed
- Deprecated API endpoints
```

## Quick Reference

### Naming Checklist
- [ ] Variables and functions: `snake_case`
- [ ] Classes: `PascalCase`
- [ ] Constants: `UPPER_SNAKE_CASE`
- [ ] Files and directories: `snake_case`
- [ ] URLs: `kebab-case`
- [ ] Templates: `snake_case.html`
- [ ] CSS classes: `kebab-case` or BEM
- [ ] Database fields: `snake_case`
- [ ] Boolean fields: `is_`, `has_`, `can_`

### Code Quality Tools

```bash
# Install development tools
pip install black isort flake8 pylint

# Format code
black .
isort .

# Check style
flake8 .
pylint project_name/
```

### VS Code Settings
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.rulers": [88]
    }
}
```

## Resources

- [PEP 8 – Style Guide for Python Code](https://pep8.org/)
- [Django Coding Style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Code Formatter](https://black.readthedocs.io/)
- [BEM Methodology](http://getbem.com/)

---

*This style guide should be considered a living document and updated as the project evolves.*
