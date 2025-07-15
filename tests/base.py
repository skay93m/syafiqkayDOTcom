# tests/base.py
"""
Base test classes for Test-Driven Development.
Provides common functionality for all test cases.
"""
import pytest
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .factories import UserFactory, SuperUserFactory


class BaseTestCase(TestCase):
    """Base test case with common setup for all tests."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
    
    def setUp(self):
        """Set up test data before each test method."""
        self.user = UserFactory()
        self.superuser = SuperUserFactory()
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def assertRedirectsTo(self, response, url_name, *args, **kwargs):
        """Assert that response redirects to a specific URL name."""
        expected_url = reverse(url_name, args=args, kwargs=kwargs)
        self.assertRedirects(response, expected_url)
    
    def assertContainsText(self, response, text):
        """Assert that response contains specific text."""
        self.assertContains(response, text)
    
    def assertNotContainsText(self, response, text):
        """Assert that response does not contain specific text."""
        self.assertNotContains(response, text)


class BaseViewTestCase(BaseTestCase):
    """Base test case for view testing."""
    
    def setUp(self):
        super().setUp()
        self.login_user = None
    
    def login(self, user=None):
        """Log in a user for testing."""
        if user is None:
            user = self.user
        self.client.force_login(user)
        self.login_user = user
    
    def logout(self):
        """Log out the current user."""
        self.client.logout()
        self.login_user = None
    
    def get_url(self, url_name, *args, **kwargs):
        """Get URL by name with optional parameters."""
        return reverse(url_name, args=args, kwargs=kwargs)
    
    def get_response(self, url_name, *args, **kwargs):
        """Make GET request to URL name."""
        url = self.get_url(url_name, *args, **kwargs)
        return self.client.get(url)
    
    def post_response(self, url_name, data=None, *args, **kwargs):
        """Make POST request to URL name."""
        url = self.get_url(url_name, *args, **kwargs)
        return self.client.post(url, data or {})


class BaseModelTestCase(BaseTestCase):
    """Base test case for model testing."""
    
    def assertModelFieldExists(self, model, field_name):
        """Assert that a model has a specific field."""
        self.assertTrue(
            hasattr(model, field_name),
            f"Model {model.__name__} should have field {field_name}"
        )
    
    def assertModelStringRepresentation(self, instance, expected_str):
        """Assert that model's string representation matches expected."""
        self.assertEqual(str(instance), expected_str)
    
    def assertModelSave(self, instance):
        """Assert that model instance can be saved."""
        try:
            instance.save()
            self.assertIsNotNone(instance.pk)
        except Exception as e:
            self.fail(f"Model save failed: {e}")


@pytest.mark.django_db
class BasePytestCase:
    """Base pytest class for Django tests."""
    
    def setup_method(self):
        """Set up test data before each test method."""
        self.user = UserFactory()
        self.superuser = SuperUserFactory()
        self.client = Client()
    
    def teardown_method(self):
        """Clean up after each test method."""
        pass
