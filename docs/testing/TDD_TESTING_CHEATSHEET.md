# TDD Testing Cheatsheet

## Table of Contents
- [TDD Principles](#tdd-principles)
- [Test Structure](#test-structure)
- [Django Testing Framework](#django-testing-framework)
- [Pytest Framework](#pytest-framework)
- [Common Test Patterns](#common-test-patterns)
- [Test Types](#test-types)
- [Assertions Reference](#assertions-reference)
- [Mocking](#mocking)
- [Database Testing](#database-testing)
- [HTTP Testing](#http-testing)
- [Running Tests](#running-tests)
- [Best Practices](#best-practices)

## TDD Principles

### Red-Green-Refactor Cycle
1. **Red**: Write a failing test
2. **Green**: Write minimal code to make it pass
3. **Refactor**: Improve code while keeping tests passing

### Test-First Development
```python
def test_user_can_create_task(self):
    # Test fails - feature doesn't exist yet
    task = Task.objects.create(title="Test Task")
    self.assertEqual(task.title, "Test Task")
```

## Test Structure

### Django Test Class Structure
```python
from django.test import TestCase
from tests.base import BaseViewTestCase

class YourFeatureTests(BaseViewTestCase):
    def setUp(self):
        """Run before each test method"""
        super().setUp()
        self.url = reverse('app:view_name')
    
    def tearDown(self):
        """Run after each test method"""
        pass
    
    def test_feature_behavior(self):
        """Test description in docstring"""
        # Arrange
        expected_result = "expected"
        
        # Act
        actual_result = some_function()
        
        # Assert
        self.assertEqual(actual_result, expected_result)
```

### Pytest Class Structure
```python
import pytest
from django.test import Client

@pytest.mark.django_db
class TestYourFeature:
    def setup_method(self):
        """Run before each test method"""
        self.client = Client()
    
    def test_feature_behavior(self):
        """Test description"""
        # Arrange, Act, Assert
        assert actual == expected
```

## Django Testing Framework

### Basic Test Class
```python
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User

class MyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_example(self):
        response = self.client.get('/path/')
        self.assertEqual(response.status_code, 200)
```

### Test Client Usage
```python
# GET request
response = self.client.get('/path/')

# POST request with data
response = self.client.post('/path/', {
    'field1': 'value1',
    'field2': 'value2'
})

# Login user
self.client.login(username='testuser', password='testpass123')

# Force login (bypass authentication)
self.client.force_login(self.user)
```

## Pytest Framework

### Basic Pytest Test
```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
def test_homepage_returns_200():
    client = Client()
    response = client.get(reverse('homepage:homepage'))
    assert response.status_code == 200
```

### Pytest Fixtures
```python
@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def client():
    return Client()

def test_with_fixtures(client, user):
    client.force_login(user)
    response = client.get('/protected/')
    assert response.status_code == 200
```

### Parametrized Tests
```python
@pytest.mark.parametrize(
    "method,expected_status",
    [
        ("GET", 200),
        ("POST", 405),
        ("PUT", 405),
        ("DELETE", 405),
    ]
)
def test_http_methods(method, expected_status):
    client = Client()
    response = getattr(client, method.lower())('/path/')
    assert response.status_code == expected_status
```

## Common Test Patterns

### View Testing Pattern
```python
class ViewTests(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('app:view_name')
    
    def test_view_url_exists(self):
        """Test URL accessibility"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test correct template usage"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'app/template.html')
    
    def test_view_contains_expected_content(self):
        """Test response content"""
        response = self.client.get(self.url)
        self.assertContains(response, 'Expected text')
    
    def test_view_with_authenticated_user(self):
        """Test with logged in user"""
        self.login()  # From BaseViewTestCase
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
```

### Model Testing Pattern
```python
class ModelTests(BaseModelTestCase):
    def test_model_creation(self):
        """Test model can be created"""
        instance = MyModel.objects.create(
            field1='value1',
            field2='value2'
        )
        self.assertEqual(instance.field1, 'value1')
    
    def test_model_string_representation(self):
        """Test model __str__ method"""
        instance = MyModel(field1='test')
        self.assertEqual(str(instance), 'test')
    
    def test_model_validation(self):
        """Test model validation"""
        with self.assertRaises(ValidationError):
            MyModel.objects.create(field1='invalid')
```

### Form Testing Pattern
```python
class FormTests(TestCase):
    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'field1': 'valid_value',
            'field2': 'another_value'
        }
        form = MyForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_data(self):
        """Test form with invalid data"""
        form_data = {'field1': ''}  # Required field empty
        form = MyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('field1', form.errors)
```

## Test Types

### Unit Tests
```python
def test_function_returns_correct_value(self):
    """Test individual function"""
    result = my_function(input_value)
    self.assertEqual(result, expected_value)
```

### Integration Tests
```python
@pytest.mark.django_db
class TestIntegration:
    def test_full_workflow(self):
        """Test complete user workflow"""
        # Create user
        user = User.objects.create_user('test', 'test@example.com', 'pass')
        
        # Login
        client = Client()
        client.force_login(user)
        
        # Perform actions
        response = client.post('/create/', {'title': 'Test'})
        
        # Verify results
        assert response.status_code == 302
        assert MyModel.objects.filter(title='Test').exists()
```

### End-to-End Tests
```python
def test_complete_user_journey(self):
    """Test complete user journey"""
    # Registration
    response = self.client.post('/register/', {
        'username': 'newuser',
        'password1': 'complexpass123',
        'password2': 'complexpass123'
    })
    
    # Login
    self.client.login(username='newuser', password='complexpass123')
    
    # Use feature
    response = self.client.get('/dashboard/')
    self.assertEqual(response.status_code, 200)
```

## Assertions Reference

### Django Assertions
```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Truth values
self.assertTrue(condition)
self.assertFalse(condition)

# None checks
self.assertIsNone(value)
self.assertIsNotNone(value)

# Type checks
self.assertIsInstance(obj, cls)

# Collections
self.assertIn(item, container)
self.assertNotIn(item, container)

# Exceptions
self.assertRaises(Exception, function, *args)
with self.assertRaises(Exception):
    function_that_raises()

# HTTP Response
self.assertContains(response, text)
self.assertNotContains(response, text)
self.assertRedirects(response, expected_url)
self.assertTemplateUsed(response, template_name)

# Database
self.assertQuerysetEqual(qs, values)
```

### Pytest Assertions
```python
# Basic assertions
assert a == b
assert a != b
assert condition
assert not condition

# With custom messages
assert a == b, f"Expected {b}, got {a}"

# Exceptions
with pytest.raises(ValueError):
    function_that_raises()

# Approximate equality
assert a == pytest.approx(b, rel=1e-6)
```

## Mocking

### Django Mock Usage
```python
from unittest.mock import patch, Mock

class TestWithMocks(TestCase):
    @patch('app.views.external_service')
    def test_view_with_mocked_service(self, mock_service):
        mock_service.return_value = 'mocked_result'
        
        response = self.client.get('/path/')
        
        mock_service.assert_called_once()
        self.assertEqual(response.status_code, 200)
    
    def test_with_mock_object(self):
        mock_obj = Mock()
        mock_obj.method.return_value = 'expected'
        
        result = function_using_mock(mock_obj)
        
        mock_obj.method.assert_called_once()
        self.assertEqual(result, 'expected')
```

### Pytest Mocking
```python
def test_with_mocker(mocker):
    """Using pytest-mock plugin"""
    mock_service = mocker.patch('app.views.external_service')
    mock_service.return_value = 'mocked'
    
    result = function_that_uses_service()
    
    mock_service.assert_called_once()
    assert result == 'expected'
```

## Database Testing

### Django Database Tests
```python
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings

class DatabaseTests(TestCase):
    def test_model_creation(self):
        """Test database operations"""
        obj = MyModel.objects.create(name='test')
        self.assertEqual(MyModel.objects.count(), 1)
    
    def test_model_query(self):
        """Test database queries"""
        MyModel.objects.create(name='test1')
        MyModel.objects.create(name='test2')
        
        results = MyModel.objects.filter(name__startswith='test')
        self.assertEqual(results.count(), 2)
```

### Pytest Database Tests
```python
@pytest.mark.django_db
def test_model_creation():
    """Test with database access"""
    obj = MyModel.objects.create(name='test')
    assert MyModel.objects.count() == 1

@pytest.mark.django_db(transaction=True)
def test_with_transactions():
    """Test with transaction support"""
    # Test code requiring transactions
    pass
```

## HTTP Testing

### Request Testing
```python
def test_get_request(self):
    response = self.client.get('/path/')
    self.assertEqual(response.status_code, 200)

def test_post_request(self):
    response = self.client.post('/path/', {
        'field': 'value'
    })
    self.assertEqual(response.status_code, 302)

def test_ajax_request(self):
    response = self.client.get('/api/data/', 
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    self.assertEqual(response.status_code, 200)
```

### Response Testing
```python
def test_response_content(self):
    response = self.client.get('/path/')
    self.assertContains(response, 'Expected text')
    self.assertNotContains(response, 'Unexpected text')

def test_response_json(self):
    response = self.client.get('/api/data/')
    data = response.json()
    self.assertEqual(data['status'], 'success')

def test_response_headers(self):
    response = self.client.get('/path/')
    self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
```

## Running Tests

### Command Line Options
```bash
# Run all tests
pytest

# Run specific test file
pytest homepage/tests.py

# Run specific test class
pytest homepage/tests.py::HomepageViewTests

# Run specific test method
pytest homepage/tests.py::HomepageViewTests::test_homepage_url_exists

# Run with coverage
pytest --cov=.

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "test_homepage"

# Run Django tests
python manage.py test

# Run specific Django test
python manage.py test homepage.tests.HomepageViewTests.test_homepage_url_exists
```

### Test Configuration (pytest.ini)
```ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
addopts = --verbose --tb=short --cov=. --cov-report=term-missing
testpaths = tests
python_files = test_*.py *_test.py tests.py
python_classes = Test*
python_functions = test_*
markers =
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    slow: marks tests as slow tests
```

## Best Practices

### Test Organization
- **One test per behavior**: Each test should verify one specific behavior
- **Descriptive names**: Test names should clearly describe what they test
- **Arrange-Act-Assert**: Structure tests with clear setup, action, and verification
- **Independent tests**: Tests should not depend on each other

### Test Data
- **Use factories**: Create test data with factory_boy or similar
- **Minimal data**: Create only the data needed for the test
- **Realistic data**: Use realistic but not production data

### Test Maintenance
- **Keep tests simple**: Tests should be easy to understand and maintain
- **Update tests with code**: Keep tests in sync with code changes
- **Remove obsolete tests**: Delete tests for removed features
- **Refactor tests**: Apply same refactoring principles to test code

### Performance
- **Use appropriate test types**: Unit tests for fast feedback, integration tests for confidence
- **Mock external dependencies**: Don't hit real APIs or external services
- **Use fixtures wisely**: Reuse common setup but avoid over-coupling

### TDD Workflow
1. Write the test first (it should fail)
2. Write minimal code to make it pass
3. Refactor both code and tests
4. Repeat for next feature

### Common Patterns
```python
# Test placeholder for TDD
def test_future_feature(self):
    """Placeholder for future feature"""
    # This test will fail until feature is implemented
    # Following TDD: Red -> Green -> Refactor
    pass

# Test error conditions
def test_invalid_input_raises_error(self):
    with self.assertRaises(ValidationError):
        function_with_invalid_input()

# Test edge cases
def test_empty_input(self):
    result = function_with_empty_input("")
    self.assertEqual(result, expected_empty_result)
```

## Quick Reference

### Test File Structure
```
tests/
├── __init__.py
├── base.py              # Base test classes
├── factories.py         # Test data factories
├── test_models.py       # Model tests
├── test_views.py        # View tests
├── test_forms.py        # Form tests
└── test_utils.py        # Utility tests

app/
├── tests.py            # App-specific tests
└── test_*.py           # Additional test files
```

### Essential Imports
```python
# Django testing
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Pytest
import pytest
from pytest import mark

# Mocking
from unittest.mock import Mock, patch, MagicMock

# Base classes (your project)
from tests.base import BaseViewTestCase, BaseModelTestCase
```

Remember: **Test-driven development is about writing tests first, then code to make them pass!**
