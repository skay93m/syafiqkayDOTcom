# Task Manager Tests

## Overview

Based on the test-driven development (TDD) approach, this document outlines the structure and usage of tests within the Task Manager application. The tests are designed to ensure that the application's functionality works as expected and to catch any regressions in future development.

## Usage

### Writing Tests

1. **Identify the functionality to test**: Before writing a test, you need to know what functionality you want to verify. This could be a specific function, a view, or a model method.

2. **Create a test case**: In your `tests.py` file, create a new test case class that inherits from `django.test.TestCase`.

3. **Write test methods**: Inside your test case class, write methods that start with `test_`. Each method should test a specific aspect of the functionality.

4. **Use assertions**: Use Django's built-in assertions (e.g., `self.assertEqual()`, `self.assertTrue()`) to verify the expected outcomes.

5. **Run your tests**: Use the Django test runner to execute your tests and see if they pass.

### Running Tests

To run your tests, use the following command:

```bash
python manage.py test
```

This will discover and run all tests in your project. You can also specify a particular app or test case to run:

```bash
python manage.py test taskmanager
```

```bash
python manage.py test taskmanager.tests.TaskTests
```

```bash
python manage.py test taskmanager.tests.SprintTests
```

```bash
python manage.py test taskmanager.tests.EpicTests
```

```bash
python manage.py test taskmanager.tests.TaskIntegrationTests
```

```bash
python manage.py test taskmanager.tests.SprintIntegrationTests
```

```bash
python manage.py test taskmanager.tests.EpicIntegrationTests
```

```bash
python manage.py test taskmanager.tests.FunctionalTests
```

## 🧪 Test Structure

### 🗂️ Folder Layout

```bash
taskmanager/
├── tests/
│   ├── __init__.py
│   ├── test_models/
│   │   ├── test_task.py
│   │   ├── test_sprint.py
│   │   └── test_epic.py
│   ├── test_views/
│   │   ├── test_task_views.py
│   │   ├── test_sprint_views.py
│   │   └── test_epic_views.py
│   ├── test_services/
│   │   ├── test_task_services.py
│   │   ├── test_sprint_services.py
│   │   └── test_epic_services.py
│   ├── test_templates/
│   │   └── test_rendering.py
│   ├── test_mixins.py
│   └── conftest.py
```
### 🧩 What Goes Where

Folder/File	Purpose
test_models/	Unit tests for model logic, constraints, and methods
test_views/	Integration tests for view behavior, routing, permissions
test_services/	Unit tests for business logic (sanitization, validation, processing)
test_templates/	Optional: test rendering, context variables, template logic
test_mixins.py	Tests for reusable mixins (e.g. sanitization, ownership checks)
conftest.py	Shared fixtures (e.g. test users, tasks, sprints)

### 🧪 Pytest Integration

Since you’re using pytest, you can take advantage of:

- **Fixtures**: Define reusable test data or setup code in `conftest.py`.
- **Markers**: Use markers to categorize tests (e.g. `@pytest.mark.task`, `@pytest.mark.sprint`).
- **Parametrization**: Easily test multiple inputs with the same test function.
- **Assertions**: Use pytest's rich assertion introspection for better error messages.

### 🧪 Example Test Case

```python
# tests/test_models/test_task.py
from django.test import TestCase
from taskmanager.models import Task
class TaskModelTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test Task", description="A task for testing")

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "A task for testing")

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task")
```

### 🧪 Example Test Case with Pytest

```python
# tests/test_models/test_task.py
import pytest
from taskmanager.models import Task
@pytest.mark.django_db
def test_task_creation():
    task = Task.objects.create(title="Test Task", description="A task for testing")
    assert task.title == "Test Task"
    assert task.description == "A task for testing"
    assert str(task) == "Test Task"
```

### 🧼 Naming Conventions

- Prefix all test files with test_
- Use descriptive test names:

```python
def test_task_title_is_sanitized():
    ...
```

### 🧠 Coverage Strategy

Use pytest-cov to track coverage:

```bash
pytest --cov=taskmanager
```

Aim for coverage across:

```python
def test_task_title_is_sanitized():
    ...
```

- Models: Ensure all model methods and properties are tested.
- Views: Test all view logic, including permissions and context.
- Services: Verify all business logic, including edge cases.
- Mixins: Test reusable components for expected behavior.
- Templates: If applicable, test rendering and context variables.
- Integration: Test end-to-end scenarios that involve multiple components.
- Functional: If applicable, test user journeys through the application.
- urls.py: Ensure all URL patterns are covered by tests.
- Error handling: Test custom error pages and triggers.
