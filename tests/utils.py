# tests/utils.py
"""
Test utilities and helpers for TDD.
Common functions used across multiple test files.
"""
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .factories import UserFactory


class TestDataHelper:
    """Helper class for creating test data."""
    
    @staticmethod
    def create_test_user(username="testuser", email="test@example.com", password="testpass123"):
        """Create a test user with default or custom attributes."""
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    
    @staticmethod
    def create_test_superuser(username="admin", email="admin@example.com", password="adminpass123"):
        """Create a test superuser with default or custom attributes."""
        return User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )


class ResponseHelper:
    """Helper class for testing HTTP responses."""
    
    @staticmethod
    def assert_response_ok(response):
        """Assert that response is successful (200)."""
        assert response.status_code == 200
    
    @staticmethod
    def assert_response_redirect(response, expected_url=None):
        """Assert that response is a redirect (302)."""
        assert response.status_code == 302
        if expected_url:
            assert response.url == expected_url
    
    @staticmethod
    def assert_response_not_found(response):
        """Assert that response is not found (404)."""
        assert response.status_code == 404
    
    @staticmethod
    def assert_response_forbidden(response):
        """Assert that response is forbidden (403)."""
        assert response.status_code == 403
    
    @staticmethod
    def assert_response_bad_request(response):
        """Assert that response is bad request (400)."""
        assert response.status_code == 400
    
    @staticmethod
    def assert_response_method_not_allowed(response):
        """Assert that response is method not allowed (405)."""
        assert response.status_code == 405


class URLHelper:
    """Helper class for working with URLs in tests."""
    
    @staticmethod
    def get_url(url_name, *args, **kwargs):
        """Get URL by name with optional parameters."""
        return reverse(url_name, args=args, kwargs=kwargs)
    
    @staticmethod
    def get_urls_for_app(app_name):
        """Get all URLs for a specific app (helper for testing)."""
        # This would need implementation based on your URL patterns
        urls = {
            'homepage': ['homepage'],
            'taskmanager': ['taskmanager:home', 'taskmanager:help'],
        }
        return urls.get(app_name, [])


class AuthHelper:
    """Helper class for authentication in tests."""
    
    @staticmethod
    def login_user(client, user):
        """Log in a user using Django test client."""
        client.force_login(user)
    
    @staticmethod
    def logout_user(client):
        """Log out current user."""
        client.logout()
    
    @staticmethod
    def create_and_login_user(client, **user_kwargs):
        """Create a user and log them in."""
        user = UserFactory(**user_kwargs)
        client.force_login(user)
        return user


class FormHelper:
    """Helper class for testing forms."""
    
    @staticmethod
    def assert_form_valid(form):
        """Assert that form is valid."""
        assert form.is_valid(), f"Form errors: {form.errors}"
    
    @staticmethod
    def assert_form_invalid(form):
        """Assert that form is invalid."""
        assert not form.is_valid()
    
    @staticmethod
    def assert_form_has_field(form, field_name):
        """Assert that form has a specific field."""
        assert field_name in form.fields
    
    @staticmethod
    def assert_form_field_required(form, field_name):
        """Assert that form field is required."""
        assert form.fields[field_name].required


class ModelHelper:
    """Helper class for testing models."""
    
    @staticmethod
    def assert_model_has_field(model_class, field_name):
        """Assert that model has a specific field."""
        assert hasattr(model_class, field_name), f"Model {model_class.__name__} should have field {field_name}"
    
    @staticmethod
    def assert_model_field_type(model_class, field_name, field_type):
        """Assert that model field is of specific type."""
        field = model_class._meta.get_field(field_name)
        assert isinstance(field, field_type), f"Field {field_name} should be of type {field_type}"
    
    @staticmethod
    def assert_model_field_max_length(model_class, field_name, max_length):
        """Assert that model field has specific max length."""
        field = model_class._meta.get_field(field_name)
        assert field.max_length == max_length
    
    @staticmethod
    def assert_model_str_representation(instance, expected_str):
        """Assert that model's string representation matches expected."""
        assert str(instance) == expected_str


class DatabaseHelper:
    """Helper class for database operations in tests."""
    
    @staticmethod
    def count_objects(model_class):
        """Count objects in database for a model."""
        return model_class.objects.count()
    
    @staticmethod
    def assert_object_exists(model_class, **kwargs):
        """Assert that object exists in database."""
        assert model_class.objects.filter(**kwargs).exists()
    
    @staticmethod
    def assert_object_does_not_exist(model_class, **kwargs):
        """Assert that object does not exist in database."""
        assert not model_class.objects.filter(**kwargs).exists()
    
    @staticmethod
    def get_object_or_fail(model_class, **kwargs):
        """Get object from database or fail test."""
        try:
            return model_class.objects.get(**kwargs)
        except model_class.DoesNotExist:
            raise AssertionError(f"Object {model_class.__name__} with {kwargs} does not exist")
        except model_class.MultipleObjectsReturned:
            raise AssertionError(f"Multiple objects {model_class.__name__} with {kwargs} found")
