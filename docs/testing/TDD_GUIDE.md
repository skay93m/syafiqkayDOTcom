# Test-Driven Development (TDD) Guide for Your Django Project

## Overview
This guide will help you implement Test-Driven Development (TDD) in your Django project. TDD is a software development approach where you write tests before writing the actual code.

## TDD Cycle: Red-Green-Refactor

### 1. 🔴 RED Phase - Write a Failing Test
- Write a test for a feature that doesn't exist yet
- The test should fail because the feature isn't implemented
- This ensures your test is actually testing something

### 2. 🟢 GREEN Phase - Make the Test Pass
- Write the minimum code needed to make the test pass
- Don't worry about perfect code, just make it work
- Focus on functionality, not optimization

### 3. 🔵 REFACTOR Phase - Improve the Code
- Clean up the code while keeping tests passing
- Improve structure, performance, and readability
- Run tests after each refactor to ensure nothing breaks

### 4. 🔄 REPEAT - Continue the Cycle
- Add more tests for edge cases and new features
- Build your application incrementally

## Project Structure

```
syafiqkaydotcom/
├── tests/                      # Project-wide test utilities
│   ├── __init__.py
│   ├── base.py                 # Base test classes
│   ├── factories.py            # Factory Boy factories
│   ├── utils.py                # Test utilities
│   └── test_environment.py     # Environment tests
├── homepage/
│   └── tests.py                # Homepage app tests
├── taskmanager/
│   └── tests.py                # Task manager app tests
├── scripts/
│   └── tdd_workflow.sh         # TDD workflow script
└── pytest.ini                 # Pytest configuration
```

## Test Types

### 1. Unit Tests
Test individual components in isolation:
```python
def test_task_model_string_representation(self):
    task = Task(title="Test Task")
    self.assertEqual(str(task), "Test Task")
```

### 2. Integration Tests
Test how components work together:
```python
@pytest.mark.django_db
def test_task_creation_with_user(self):
    user = UserFactory()
    task = TaskFactory(user=user)
    assert task.user == user
```

### 3. View Tests
Test HTTP responses and templates:
```python
def test_homepage_returns_200(self):
    response = self.client.get(reverse('homepage'))
    self.assertEqual(response.status_code, 200)
```

### 4. Model Tests
Test database models:
```python
def test_task_model_has_required_fields(self):
    task = TaskFactory()
    self.assertIsNotNone(task.title)
    self.assertIsNotNone(task.created_at)
```

## Running Tests

### Basic Test Commands

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest homepage/tests.py

# Run specific test class
poetry run pytest homepage/tests.py::HomepageViewTests

# Run specific test method
poetry run pytest homepage/tests.py::HomepageViewTests::test_homepage_returns_200

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=. --cov-report=html
```

### Using the TDD Workflow Script

```bash
# Show TDD explanation
./scripts/tdd_workflow.sh demo

# Run tests
./scripts/tdd_workflow.sh run

# Run specific test file
./scripts/tdd_workflow.sh run homepage/tests.py

# Run tests with coverage
./scripts/tdd_workflow.sh coverage

# Check test status
./scripts/tdd_workflow.sh status

# Run specific test categories
./scripts/tdd_workflow.sh category models
./scripts/tdd_workflow.sh category views
./scripts/tdd_workflow.sh category forms
```

## TDD Best Practices

### 1. Write Tests First
- Always write the test before implementing the feature
- This ensures you understand the requirements clearly

### 2. Keep Tests Simple
- One test should test one thing
- Use descriptive test names
- Keep test methods short and focused

### 3. Use Test Fixtures and Factories
- Use Factory Boy for creating test data
- Keep test data consistent and realistic

### 4. Test Edge Cases
- Test both happy path and error conditions
- Test boundary conditions and invalid inputs

### 5. Mock External Dependencies
- Mock external APIs, services, and complex dependencies
- Focus on testing your code, not external systems

## Example TDD Workflow

Let's implement a new feature using TDD:

### Step 1: Write a Failing Test (RED)
```python
# taskmanager/tests.py
def test_task_can_be_marked_as_completed(self):
    task = TaskFactory(completed=False)
    task.mark_as_completed()
    self.assertTrue(task.completed)
```

### Step 2: Run the Test (Should Fail)
```bash
poetry run pytest taskmanager/tests.py::TaskModelTests::test_task_can_be_marked_as_completed
```

### Step 3: Implement the Feature (GREEN)
```python
# taskmanager/models.py
class Task(models.Model):
    # ... existing fields ...
    
    def mark_as_completed(self):
        self.completed = True
        self.save()
```

### Step 4: Run the Test Again (Should Pass)
```bash
poetry run pytest taskmanager/tests.py::TaskModelTests::test_task_can_be_marked_as_completed
```

### Step 5: Refactor if Needed (REFACTOR)
```python
# taskmanager/models.py
class Task(models.Model):
    # ... existing fields ...
    
    def mark_as_completed(self):
        """Mark this task as completed."""
        self.completed = True
        self.updated_at = timezone.now()
        self.save()
    
    def mark_as_incomplete(self):
        """Mark this task as incomplete."""
        self.completed = False
        self.updated_at = timezone.now()
        self.save()
```

## Test Configuration

### pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = syafiqkaydotcom.settings
addopts = --verbose --tb=short --cov=. --cov-report=term-missing --cov-report=html
testpaths = tests homepage/tests.py taskmanager/tests.py
python_files = test_*.py *_test.py tests.py
python_classes = Test*
python_functions = test_*
markers =
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    slow: marks tests as slow tests
    django_db: marks tests as requiring database access
```

## Test Utilities

### Base Test Classes
- `BaseTestCase`: Common functionality for all tests
- `BaseViewTestCase`: Specialized for view testing
- `BaseModelTestCase`: Specialized for model testing

### Factories
- `UserFactory`: Creates test users
- `TaskFactory`: Creates test tasks
- `SuperUserFactory`: Creates admin users

### Helper Functions
- `ResponseHelper`: Common response assertions
- `AuthHelper`: Authentication utilities
- `ModelHelper`: Model testing utilities

## Common Test Patterns

### Testing Views
```python
def test_view_requires_authentication(self):
    response = self.client.get(self.url)
    self.assertRedirects(response, '/login/')

def test_view_with_authenticated_user(self):
    self.login()
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
```

### Testing Models
```python
def test_model_string_representation(self):
    task = TaskFactory(title="Test Task")
    self.assertEqual(str(task), "Test Task")

def test_model_creation(self):
    task = TaskFactory()
    self.assertIsNotNone(task.pk)
    self.assertIsNotNone(task.created_at)
```

### Testing Forms
```python
def test_form_valid_data(self):
    form_data = {'title': 'Test Task', 'description': 'Test Description'}
    form = TaskForm(data=form_data)
    self.assertTrue(form.is_valid())

def test_form_invalid_data(self):
    form_data = {'title': '', 'description': 'Test Description'}
    form = TaskForm(data=form_data)
    self.assertFalse(form.is_valid())
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest --cov=. --cov-report=xml
```

## Debugging Tests

### Common Issues
1. **Test database not created**: Make sure to use `@pytest.mark.django_db`
2. **Import errors**: Check your Python path and installed packages
3. **Assertion errors**: Use descriptive error messages
4. **Flaky tests**: Remove dependencies on external systems

### Debugging Tips
- Use `pytest --pdb` to drop into debugger on failures
- Use `pytest -s` to see print statements
- Use `pytest --lf` to run only the last failed tests
- Use `pytest --tb=long` for detailed tracebacks

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [TDD by Example (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

## Next Steps

1. Run the existing tests to understand the current state
2. Add tests for new features before implementing them
3. Set up continuous integration to run tests automatically
4. Aim for high test coverage (80%+ is good)
5. Review and refactor tests regularly

Remember: **Red → Green → Refactor → Repeat**
