# Complete Django Rebuild Manual

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Python Packages](#python-packages)
3. [Project Structure](#project-structure)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Key Django Patterns](#key-django-patterns)
6. [Common Challenges](#common-challenges)
7. [Reference Commands](#reference-commands)

---

## Core Concepts

### 1. Django MVT Architecture
```
Model (M) - Data layer (database models)
View (V) - Logic layer (business logic)
Template (T) - Presentation layer (HTML templates)
```

**Key Understanding:**
- Models define your data structure and relationships
- Views handle HTTP requests and return responses
- Templates render HTML with dynamic content
- URLs route requests to appropriate views

### 2. Django Apps
```
An app is a Python package that provides some set of features.
A project is a collection of apps plus configuration.
```

**Your Apps:**
- `homepage` - Main landing page, visitor tracking
- `journals` - Blog-like entries with tags
- `noto_garden` - Note-taking with linking
- `reference` - Reference management
- `experiments` - Experiment tracking

### 3. Database Relationships
```python
# One-to-Many (ForeignKey)
author = models.ForeignKey(User, on_delete=models.CASCADE)

# Many-to-Many
tags = models.ManyToManyField(Tag, blank=True)

# One-to-One
profile = models.OneToOneField(User, on_delete=models.CASCADE)
```

### 4. Django ORM (Object-Relational Mapping)
```python
# Create
Journal.objects.create(title="My Title")

# Read
journals = Journal.objects.all()
journal = Journal.objects.get(id=1)
filtered = Journal.objects.filter(title__contains="Django")

# Update
journal.title = "New Title"
journal.save()

# Delete
journal.delete()
```

### 5. Request/Response Cycle
```
1. URL dispatcher receives request
2. Calls appropriate view function
3. View processes request (database queries, logic)
4. View returns HttpResponse (often rendered template)
5. Django sends response to browser
```

---

## Python Packages

### Essential Packages
```txt
# Core Django
Django==5.0.14

# Database
dj-database-url==2.2.0      # Database URL parsing

# Environment Management
python-dotenv==1.0.1        # Load environment variables from .env

# Cloud Storage (for production)
django-storages==1.14.4     # Cloud storage backends
azure-storage-blob==12.23.1 # Azure blob storage

# Development Tools
pillow==10.4.0              # Image processing (if using ImageField)
```

### Optional Enhancement Packages
```txt
# Rich Text Editing
django-ckeditor==6.7.1

# API Development
djangorestframework==3.15.2

# Better Admin
django-admin-interface==0.28.8

# Debugging
django-debug-toolbar==4.4.6

# Testing
pytest-django==4.9.0

# Performance
django-cache-machine==1.2.0
```

### Package Purposes Explained

**dj-database-url**: Parses DATABASE_URL environment variable
```python
DATABASES = {
    'default': dj_database_url.parse(database_url, conn_max_age=600)
}
```

**python-dotenv**: Loads environment variables from .env file
```python
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
```

**django-storages**: Handles static files in cloud storage
```python
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"
```

---

## Project Structure

### Recommended File Organization
```
syafiqkay/                      # Project root
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (local)
├── db.sqlite3                  # SQLite database (development)
│
├── syafiqkay/                  # Main project package
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point (for async)
│
├── homepage/                   # Homepage app
│   ├── __init__.py
│   ├── models.py               # Database models
│   ├── views.py                # View functions/classes
│   ├── urls.py                 # App-specific URLs
│   ├── admin.py                # Admin interface
│   ├── apps.py                 # App configuration
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migrations
│       └── __init__.py
│
├── journals/                   # Journals app
│   └── [same structure as homepage]
│
├── noto_garden/                # Notes app
│   └── [same structure as homepage]
│
├── templates/                  # HTML templates
│   ├── base/
│   │   ├── index.html          # Main base template
│   │   └── head.html           # HTML head section
│   ├── components/
│   │   ├── navbar.html         # Navigation bar
│   │   └── footer.html         # Footer
│   ├── homepage/
│   │   └── homepage.html       # Homepage template
│   ├── journals/
│   │   ├── dashboard.html      # Journals list
│   │   └── detail.html         # Journal detail
│   └── [other app templates]
│
└── static/                     # Static files
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
        └── favicon.ico
```

---

## Step-by-Step Implementation

### Phase 1: Project Foundation

#### 1.1 Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install Django
pip install Django==5.0.14

# Create Django project
django-admin startproject syafiqkay .

# Create .env file
touch .env
```

#### 1.2 Basic Settings Configuration
```python
# syafiqkay/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ["true", "1", "yes"]
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Add your domain when deploying
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your apps will go here
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

#### 1.3 Create .env File
```bash
# .env
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
```

#### 1.4 Initial Migration and Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Phase 2: Homepage App

#### 2.1 Create Homepage App
```bash
python manage.py startapp homepage
```

#### 2.2 Add to INSTALLED_APPS
```python
# syafiqkay/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',  # Add this
]
```

#### 2.3 Create Homepage Models
```python
# homepage/models.py
from django.db import models
from django.utils import timezone

class Rirekisho(models.Model):
    """Resume/CV model for personal statement"""
    version = models.PositiveIntegerField(unique=True, verbose_name='Version')
    personal_statement = models.TextField(blank=True, verbose_name='Personal Statement')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        ordering = ['-version']

    def __str__(self):
        return f"Resume v{self.version}"

class VisitorTracking(models.Model):
    """Track daily visitor statistics"""
    date = models.DateField(default=timezone.now, unique=True)
    daily_visitors = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Visitors on {self.date}: {self.daily_visitors}"

class VisitorSession(models.Model):
    """Track individual visitor sessions"""
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session_key', 'date']
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.session_key} on {self.date}"
```

#### 2.4 Create and Run Migrations
```bash
python manage.py makemigrations homepage
python manage.py migrate
```

#### 2.5 Register Models in Admin
```python
# homepage/admin.py
from django.contrib import admin
from .models import Rirekisho, VisitorTracking, VisitorSession

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ('version', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('personal_statement',)

@admin.register(VisitorTracking)
class VisitorTrackingAdmin(admin.ModelAdmin):
    list_display = ('date', 'daily_visitors')
    list_filter = ('date',)
    ordering = ['-date']

@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('session_key', 'ip_address')
```

#### 2.6 Create Homepage View
```python
# homepage/views.py
from django.shortcuts import render
from .models import Rirekisho, VisitorTracking, VisitorSession
from django.utils import timezone
import datetime

def homepage(request):
    # Get latest resume
    try:
        rirekisho = Rirekisho.objects.latest('version')
    except Rirekisho.DoesNotExist:
        rirekisho = None
    
    # Track visitor (simplified version)
    track_visitor(request)
    
    # Get statistics
    today = timezone.now().date()
    try:
        today_stats = VisitorTracking.objects.get(date=today)
        daily_visitors = today_stats.daily_visitors
    except VisitorTracking.DoesNotExist:
        daily_visitors = 0
    
    # Calculate total visitors
    total_visitors = sum(vt.daily_visitors for vt in VisitorTracking.objects.all())
    
    # Calculate weekly visitors
    week_ago = today - datetime.timedelta(days=7)
    weekly_visitors = sum(
        vt.daily_visitors 
        for vt in VisitorTracking.objects.filter(date__gte=week_ago)
    )
    
    context = {
        'rirekisho': rirekisho,
        'statistics': {
            'daily_visitors': daily_visitors,
            'total_visitors': total_visitors,
            'weekly_visitors': weekly_visitors,
            'today_date': today,
        }
    }
    
    return render(request, 'homepage/homepage.html', context)

def track_visitor(request):
    """Simple visitor tracking"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    today = timezone.now().date()
    
    # Check if this session was already tracked today
    visitor_session, created = VisitorSession.objects.get_or_create(
        session_key=session_key,
        date=today,
        defaults={
            'ip_address': ip_address,
            'user_agent': user_agent,
        }
    )
    
    if created:
        # Update daily visitor count
        visitor_tracking, created = VisitorTracking.objects.get_or_create(
            date=today,
            defaults={'daily_visitors': 0}
        )
        visitor_tracking.daily_visitors += 1
        visitor_tracking.save()

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
```

#### 2.7 Create URLs
```python
# homepage/urls.py
from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]
```

```python
# syafiqkay/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
]
```

#### 2.8 Create Base Template
```html
<!-- templates/base/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Syafiq Kay - Digital Dojo{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'homepage:homepage' %}">🥷 Syafiq Kay</a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'homepage:homepage' %}">Home</a>
                    </li>
                    <!-- Add more navigation items as you build other apps -->
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light mt-5 py-4">
        <div class="container text-center">
            <p>&copy; {% now "Y" %} Syafiq Kay. Built with Django 🥷</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### 2.9 Create Homepage Template
```html
<!-- templates/homepage/homepage.html -->
{% extends "base/index.html" %}
{% load static %}

{% block content %}
<div class="container mt-5">
    <!-- Header Section -->
    <div class="text-center mb-5">
        <h1 class="display-4 mb-3">🥷 Digital Dojo 🥷</h1>
        <p class="lead">Where ancient wisdom meets modern technology in the pursuit of mastery.</p>
    </div>

    <!-- Personal Statement Section -->
    {% if rirekisho %}
    <div class="row mb-5">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="card-title mb-0">🥷 Personal Statement</h4>
                </div>
                <div class="card-body">
                    <div class="card-text">{{ rirekisho.personal_statement|linebreaks }}</div>
                    <div class="text-muted">
                        <small>
                            📅 Created: {{ rirekisho.created_at|date:"M d, Y H:i" }}
                            {% if rirekisho.updated_at != rirekisho.created_at %}
                                | Updated: {{ rirekisho.updated_at|date:"M d, Y H:i" }}
                            {% endif %}
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endif %}

    <!-- Statistics Section -->
    <div class="row mb-5">
        <div class="col-12">
            <h3 class="mb-4 text-center">📊 Dojo Statistics</h3>
        </div>
    </div>
    
    <!-- Statistics Cards -->
    <div class="row mb-5">
        <div class="col-md-4">
            <div class="card border">
                <div class="card-body text-center">
                    <h3 class="card-title text-primary">{{ statistics.daily_visitors }}</h3>
                    <p class="card-text">Today's Visitors</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border">
                <div class="card-body text-center">
                    <h3 class="card-title text-success">{{ statistics.total_visitors }}</h3>
                    <p class="card-text">Total Visitors</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border">
                <div class="card-body text-center">
                    <h3 class="card-title text-warning">{{ statistics.weekly_visitors }}</h3>
                    <p class="card-text">Weekly Visitors</p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    border-radius: 0.5rem;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
{% endblock %}
```

#### 2.10 Create Basic CSS
```css
/* static/css/style.css */
/* Custom styles for your Django application */

.navbar-brand {
    font-weight: bold;
}

.card {
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
}

.card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.btn {
    border-radius: 0.375rem;
}

/* Japanese text styling */
.jp-text {
    font-size: 0.9em;
    color: #666;
    font-style: italic;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .display-4 {
        font-size: 2rem;
    }
}
```

### Phase 3: Journals App (Example Structure)

#### 3.1 Create Journals App
```bash
python manage.py startapp journals
```

#### 3.2 Journal Model Example
```python
# journals/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Journal(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, help_text="Brief summary of the journal entry")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('journals:detail', kwargs={'pk': self.pk})

    def get_tags(self):
        """Return list of tags"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
```

---

## Key Django Patterns

### 1. Model Patterns
```python
# Always include __str__ method
def __str__(self):
    return self.title

# Use Meta class for model options
class Meta:
    ordering = ['-created_at']
    verbose_name = 'Journal Entry'
    verbose_name_plural = 'Journal Entries'

# Add helper methods
def get_absolute_url(self):
    return reverse('app:detail', kwargs={'pk': self.pk})
```

### 2. View Patterns
```python
# Function-based views
def my_view(request):
    context = {'data': 'value'}
    return render(request, 'template.html', context)

# Class-based views
from django.views.generic import ListView, DetailView

class JournalListView(ListView):
    model = Journal
    template_name = 'journals/list.html'
    context_object_name = 'journals'
    paginate_by = 10
```

### 3. URL Patterns
```python
# Use app namespaces
app_name = 'journals'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.detail, name='detail'),
]

# In templates: {% url 'journals:dashboard' %}
```

### 4. Template Patterns
```html
<!-- Template inheritance -->
{% extends "base/index.html" %}

<!-- Load static files -->
{% load static %}

<!-- Use blocks for customization -->
{% block title %}Custom Title{% endblock %}

{% block content %}
<!-- Your content here -->
{% endblock %}

<!-- Template filters -->
{{ journal.created_at|date:"M d, Y" }}
{{ journal.content|truncatewords:50 }}
```

---

## Common Challenges

### 1. Migration Issues
```bash
# If migrations conflict:
python manage.py makemigrations --merge

# Reset migrations (development only):
rm -rf app/migrations/
python manage.py makemigrations app
python manage.py migrate
```

### 2. Static Files Not Loading
```python
# In development settings:
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# In templates:
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

### 3. Template Not Found
- Check TEMPLATES setting in settings.py
- Ensure template path is correct
- Check template inheritance hierarchy

### 4. Import Errors
```python
# Use relative imports in apps:
from .models import MyModel  # Same app
from django.contrib.auth.models import User  # Django built-in
```

---

## Reference Commands

### Django Management
```bash
# Start new project
django-admin startproject projectname

# Start new app
python manage.py startapp appname

# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# User management
python manage.py createsuperuser
python manage.py changepassword username

# Development server
python manage.py runserver
python manage.py runserver 8080  # Custom port

# Django shell
python manage.py shell

# Check for issues
python manage.py check

# Collect static files (production)
python manage.py collectstatic
```

### Useful Django Shell Commands
```python
# In Django shell (python manage.py shell)
from homepage.models import Rirekisho

# Create object
r = Rirekisho.objects.create(version=1, personal_statement="Test")

# Query objects
all_resumes = Rirekisho.objects.all()
latest = Rirekisho.objects.latest('version')

# Filter objects
filtered = Rirekisho.objects.filter(version__gte=1)

# Update objects
r.personal_statement = "Updated statement"
r.save()
```

### Git Commands for Reference
```bash
# View file from main branch
git show main:path/to/file

# Compare with main branch
git diff main -- path/to/file

# Switch branches
git checkout main           # View reference
git checkout manual-rebuild # Back to development
```

---

This manual should give you everything you need to rebuild the application from scratch while understanding each component deeply. Start with the foundation and build up gradually!
