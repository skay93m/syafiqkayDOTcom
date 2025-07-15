# Environment Testing Guide

This document provides a comprehensive walkthrough for creating tests to verify that your Poetry and Django environment is set up correctly.

## Table of Contents
1. [Overview](#overview)
2. [Test Structure](#test-structure)
3. [Poetry Environment Tests](#poetry-environment-tests)
4. [Django Environment Tests](#django-environment-tests)
5. [Database Connection Tests](#database-connection-tests)
6. [Dependency Tests](#dependency-tests)
7. [Configuration Tests](#configuration-tests)
8. [Running Tests](#running-tests)
9. [CI/CD Integration](#cicd-integration)

---

## Overview

### Why Environment Testing?

Environment tests ensure that:
- ✅ Python environment is correctly configured
- ✅ All dependencies are properly installed
- ✅ Django settings are valid
- ✅ Database connections work
- ✅ Required environment variables are set
- ✅ File permissions are correct

### Test Types

1. **Poetry Environment Tests** - Verify virtual environment and dependencies
2. **Django Configuration Tests** - Validate Django settings and apps
3. **Database Tests** - Check database connectivity and migrations
4. **Integration Tests** - Test component interactions
5. **Health Check Tests** - Overall system health verification

---

## Test Structure

### Recommended Directory Structure

```
your_project/
├── tests/
│   ├── __init__.py
│   ├── test_environment.py           # Environment setup tests
│   ├── test_dependencies.py          # Dependency verification
│   ├── test_django_config.py         # Django configuration tests
│   ├── test_database.py              # Database connection tests
│   └── conftest.py                   # Pytest configuration
├── scripts/
│   └── test_environment.py           # Standalone environment checker
└── pyproject.toml                    # Test configuration
```

---

## Poetry Environment Tests

### File: `tests/test_environment.py`

#### 1. Python Version Test

```python
import sys
import pytest

def test_python_version():
    """Test that Python version meets project requirements."""
    required_version = (3, 12)  # Adjust based on your pyproject.toml
    current_version = sys.version_info[:2]
    
    assert current_version >= required_version, (
        f"Python {'.'.join(map(str, required_version))}+ required, "
        f"but {'.'.join(map(str, current_version))} found"
    )

def test_python_executable_path():
    """Test that we're using the correct Python executable."""
    import os
    
    # Should be in virtual environment
    executable = sys.executable
    
    # Check if we're in a virtual environment
    assert (
        'virtualenvs' in executable or 
        'venv' in executable or 
        os.environ.get('VIRTUAL_ENV')
    ), f"Not running in virtual environment. Using: {executable}"
```

#### 2. Virtual Environment Test

```python
import os
import subprocess

def test_virtual_environment():
    """Test that we're running in a Poetry virtual environment."""
    # Check VIRTUAL_ENV environment variable
    virtual_env = os.environ.get('VIRTUAL_ENV')
    assert virtual_env is not None, "VIRTUAL_ENV not set"
    
    # Verify it's a Poetry environment
    assert 'poetry' in virtual_env.lower(), (
        f"Not a Poetry virtual environment: {virtual_env}"
    )

def test_poetry_installation():
    """Test that Poetry is installed and accessible."""
    try:
        result = subprocess.run(
            ['poetry', '--version'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        assert 'Poetry' in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("Poetry is not installed or not accessible")

def test_poetry_environment_info():
    """Test that Poetry environment information is accessible."""
    try:
        result = subprocess.run(
            ['poetry', 'env', 'info'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        assert 'Python:' in result.stdout
        assert 'Path:' in result.stdout
        assert 'Valid: True' in result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Cannot get Poetry environment info")
```

---

## Django Environment Tests

### File: `tests/test_django_config.py`

#### 1. Django Import and Setup Test

```python
import os
import django
from django.conf import settings
from django.test import TestCase

def test_django_import():
    """Test that Django can be imported."""
    try:
        import django
        assert hasattr(django, 'VERSION')
    except ImportError:
        pytest.fail("Django is not installed or not importable")

def test_django_settings():
    """Test that Django settings are properly configured."""
    # Set Django settings module if not already set
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syafiqkaydotcom.settings')
    
    try:
        django.setup()
    except Exception as e:
        pytest.fail(f"Django setup failed: {e}")
    
    # Test basic settings
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'DATABASES')
    assert hasattr(settings, 'INSTALLED_APPS')

def test_installed_apps():
    """Test that all required Django apps are installed."""
    required_apps = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'taskmanager',  # Your custom app
    ]
    
    for app in required_apps:
        assert app in settings.INSTALLED_APPS, (
            f"Required app '{app}' not in INSTALLED_APPS"
        )
```

#### 2. Django Management Commands Test

```python
import subprocess
import os

def test_django_check():
    """Test Django's system check framework."""
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'syafiqkaydotcom.settings'
    
    try:
        result = subprocess.run(
            ['python', 'manage.py', 'check'],
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        # Should have no critical issues
        assert 'System check identified no issues' in result.stdout or \
               result.returncode == 0
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Django check failed: {e.stderr}")

def test_collect_static():
    """Test that static files can be collected."""
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'syafiqkaydotcom.settings'
    
    try:
        result = subprocess.run(
            ['python', 'manage.py', 'collectstatic', '--dry-run', '--noinput'],
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        assert result.returncode == 0
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Static files collection failed: {e.stderr}")
```

---

## Database Connection Tests

### File: `tests/test_database.py`

#### 1. Database Configuration Test

```python
from django.db import connections, connection
from django.core.exceptions import ImproperlyConfigured
import pytest

def test_database_configuration():
    """Test that database is properly configured."""
    try:
        db_config = connection.settings_dict
        
        # Check required database settings
        assert 'ENGINE' in db_config
        assert 'NAME' in db_config
        
        # Verify engine is supported
        supported_engines = [
            'django.db.backends.postgresql',
            'django.db.backends.sqlite3',
            'mssql',  # For your MSSQL setup
        ]
        
        engine = db_config['ENGINE']
        assert any(supported in engine for supported in supported_engines), (
            f"Unsupported database engine: {engine}"
        )
        
    except ImproperlyConfigured as e:
        pytest.fail(f"Database configuration error: {e}")

def test_database_connection():
    """Test that database connection can be established."""
    try:
        # Test connection
        connection.ensure_connection()
        
        # Test cursor operations
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
            
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_database_migrations():
    """Test that migrations are up to date."""
    from django.core.management import execute_from_command_line
    import io
    import sys
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
        output = captured_output.getvalue()
        
        # Should not have unapplied migrations
        assert '[ ]' not in output, "Unapplied migrations found"
        
    except SystemExit:
        pass  # Normal exit from management command
    finally:
        sys.stdout = old_stdout
```

---

## Dependency Tests

### File: `tests/test_dependencies.py`

#### 1. Required Package Tests

```python
import importlib
import pkg_resources

def test_required_packages():
    """Test that all required packages are installed."""
    required_packages = [
        'django',
        'requests',
        'pyodbc',
        'python-dotenv',
        'psycopg',
        'mssql-django',
        'pytest',  # Development dependency
    ]
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
        except ImportError:
            pytest.fail(f"Required package '{package}' is not installed")

def test_package_versions():
    """Test that packages meet version requirements."""
    version_requirements = {
        'django': '5.0.14',
        'requests': '2.32.4',
        'pytest': '8.4.1',
    }
    
    for package, required_version in version_requirements.items():
        try:
            installed_version = pkg_resources.get_distribution(package).version
            
            # Basic version check (you might want more sophisticated comparison)
            major_minor_required = '.'.join(required_version.split('.')[:2])
            major_minor_installed = '.'.join(installed_version.split('.')[:2])
            
            assert major_minor_installed >= major_minor_required, (
                f"{package} version {installed_version} does not meet "
                f"requirement {required_version}"
            )
        except pkg_resources.DistributionNotFound:
            pytest.fail(f"Package '{package}' is not installed")

def test_conflicting_packages():
    """Test for known package conflicts."""
    # Add any known conflicting packages here
    conflicts = [
        # Example: ('package1', 'package2')
    ]
    
    installed_packages = [pkg.project_name for pkg in pkg_resources.working_set]
    
    for pkg1, pkg2 in conflicts:
        if pkg1 in installed_packages and pkg2 in installed_packages:
            pytest.fail(f"Conflicting packages detected: {pkg1} and {pkg2}")
```

---

## Configuration Tests

### File: `tests/test_configuration.py`

#### 1. Environment Variables Test

```python
import os

def test_required_environment_variables():
    """Test that required environment variables are set."""
    required_env_vars = [
        'DJANGO_SETTINGS_MODULE',
        # Add other required environment variables
    ]
    
    for var in required_env_vars:
        assert os.environ.get(var) is not None, (
            f"Required environment variable '{var}' is not set"
        )

def test_secret_key():
    """Test that Django SECRET_KEY is properly configured."""
    from django.conf import settings
    
    assert hasattr(settings, 'SECRET_KEY')
    assert len(settings.SECRET_KEY) >= 50, "SECRET_KEY is too short"
    assert settings.SECRET_KEY != 'your-secret-key-here', (
        "SECRET_KEY is set to default value"
    )

def test_debug_setting():
    """Test DEBUG setting based on environment."""
    from django.conf import settings
    
    # In production, DEBUG should be False
    # You can adjust this based on your environment detection logic
    if os.environ.get('DJANGO_ENV') == 'production':
        assert not settings.DEBUG, "DEBUG should be False in production"
```

#### 2. File Permissions Test

```python
import os
import stat

def test_file_permissions():
    """Test that critical files have correct permissions."""
    files_to_check = [
        'manage.py',
        'scripts/commit.sh',
        'scripts/setup-commitizen.sh',
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            file_stat = os.stat(file_path)
            # Check if file is executable by owner
            assert file_stat.st_mode & stat.S_IXUSR, (
                f"File '{file_path}' is not executable"
            )

def test_directory_structure():
    """Test that required directories exist."""
    required_dirs = [
        'syafiqkaydotcom',
        'taskmanager',
        'templates',
        'scripts',
        'docs',
    ]
    
    for directory in required_dirs:
        assert os.path.isdir(directory), (
            f"Required directory '{directory}' does not exist"
        )
```

---

## Running Tests

### Pytest Configuration

Create `pyproject.toml` test configuration:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "syafiqkaydotcom.settings"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
testpaths = ["tests"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--disable-warnings",
]
markers = [
    "environment: Environment setup tests",
    "database: Database connection tests",
    "dependencies: Package dependency tests",
    "slow: Slow running tests",
]
```

### Running Tests

```bash
# Run all environment tests
poetry run pytest tests/

# Run specific test file
poetry run pytest tests/test_environment.py -v

# Run tests with specific markers
poetry run pytest -m environment

# Run tests with coverage
poetry run pytest --cov=. tests/

# Run tests and generate HTML coverage report
poetry run pytest --cov=. --cov-report=html tests/
```

### Standalone Environment Checker

Create `scripts/test_environment.py`:

```python
#!/usr/bin/env python3
"""
Standalone environment checker script.
Run this to quickly verify environment setup.
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    required = (3, 12)
    current = sys.version_info[:2]
    
    if current >= required:
        print(f"   ✅ Python {'.'.join(map(str, current))} (required: {'.'.join(map(str, required))}+)")
        return True
    else:
        print(f"   ❌ Python {'.'.join(map(str, current))} (required: {'.'.join(map(str, required))}+)")
        return False

def check_virtual_environment():
    """Check if running in virtual environment."""
    print("📦 Checking virtual environment...")
    
    if os.environ.get('VIRTUAL_ENV'):
        venv_path = os.environ['VIRTUAL_ENV']
        print(f"   ✅ Virtual environment: {venv_path}")
        return True
    else:
        print("   ❌ Not running in virtual environment")
        return False

def check_poetry():
    """Check Poetry installation."""
    print("🎭 Checking Poetry...")
    
    try:
        result = subprocess.run(['poetry', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Poetry error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("   ❌ Poetry not found")
        return False

def check_dependencies():
    """Check key dependencies."""
    print("📚 Checking dependencies...")
    
    packages = ['django', 'requests', 'pytest']
    all_good = True
    
    for package in packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {package} ({version})")
        except ImportError:
            print(f"   ❌ {package} not found")
            all_good = False
    
    return all_good

def check_django():
    """Check Django configuration."""
    print("🎸 Checking Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syafiqkaydotcom.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"   ✅ Django {django.VERSION[:3]} configured")
        
        # Test database connection
        from django.db import connection
        connection.ensure_connection()
        print("   ✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Django error: {e}")
        return False

def main():
    """Run all checks."""
    print("🔍 Environment Health Check")
    print("=" * 30)
    
    checks = [
        check_python_version,
        check_virtual_environment,
        check_poetry,
        check_dependencies,
        check_django,
    ]
    
    results = []
    for check in checks:
        results.append(check())
        print()
    
    print("📊 Summary")
    print("-" * 20)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        sys.exit(0)
    else:
        print(f"⚠️  Some checks failed ({passed}/{total})")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

Make it executable:
```bash
chmod +x scripts/test_environment.py
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/test-environment.yml`:

```yaml
name: Environment Tests

on: [push, pull_request]

jobs:
  test-environment:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run environment tests
      run: poetry run pytest tests/test_environment.py -v
    
    - name: Run standalone checker
      run: poetry run python scripts/test_environment.py
```

### Pre-commit Hook for Tests

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
echo "🧪 Running environment tests..."

# Run quick environment check
poetry run python scripts/test_environment.py

if [ $? -ne 0 ]; then
    echo "❌ Environment tests failed. Commit aborted."
    exit 1
fi

echo "✅ Environment tests passed."
```

---

## Summary

This testing strategy ensures:

1. **Environment Validation** - Python, Poetry, virtual environment
2. **Django Configuration** - Settings, apps, management commands
3. **Database Connectivity** - Connection, migrations, operations
4. **Dependency Management** - Required packages, versions, conflicts
5. **Configuration Verification** - Environment variables, file permissions
6. **Continuous Testing** - CI/CD integration, pre-commit hooks

### Quick Start Checklist

- [ ] Create test directory structure
- [ ] Write environment tests for your specific setup
- [ ] Configure pytest in pyproject.toml
- [ ] Create standalone environment checker
- [ ] Set up CI/CD workflow
- [ ] Add pre-commit hooks for automated testing

Run these tests regularly to catch environment issues early and ensure consistent setup across different machines and deployments.
