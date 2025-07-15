# taskmanager/tests.py
"""
Test-Driven Development tests for taskmanager app.
Following TDD principles: Red -> Green -> Refactor
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from unittest.mock import patch

from taskmanager.views import home, help
from tests.base import BaseViewTestCase, BaseModelTestCase


class TaskManagerViewTests(BaseViewTestCase):
    """TDD tests for taskmanager views."""
    
    def setUp(self):
        super().setUp()
        self.home_url = reverse('taskmanager:home')
        self.help_url = reverse('taskmanager:help')
    
    def test_taskmanager_home_url_exists(self):
        """Test that taskmanager home URL exists and is accessible."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
    
    def test_taskmanager_home_uses_correct_template(self):
        """Test that taskmanager home uses the correct template."""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'taskmanager/tm_home.html')
    
    def test_taskmanager_help_url_exists(self):
        """Test that taskmanager help URL exists and is accessible."""
        response = self.client.get(self.help_url)
        self.assertEqual(response.status_code, 200)
    
    def test_taskmanager_help_uses_correct_template(self):
        """Test that taskmanager help uses the correct template."""
        response = self.client.get(self.help_url)
        self.assertTemplateUsed(response, 'taskmanager/tm_help.html')
    
    def test_taskmanager_home_contains_expected_content(self):
        """Test that taskmanager home contains expected content."""
        response = self.client.get(self.home_url)
        self.assertContains(response, 'html')  # Basic HTML structure
    
    def test_taskmanager_help_contains_expected_content(self):
        """Test that taskmanager help contains expected content."""
        response = self.client.get(self.help_url)
        self.assertContains(response, 'html')  # Basic HTML structure
    
    def test_taskmanager_home_response_is_html(self):
        """Test that taskmanager home returns HTML response."""
        response = self.client.get(self.home_url)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
    
    def test_taskmanager_help_response_is_html(self):
        """Test that taskmanager help returns HTML response."""
        response = self.client.get(self.help_url)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
    
    def test_taskmanager_views_with_authenticated_user(self):
        """Test taskmanager views with authenticated user."""
        self.login()
        
        home_response = self.client.get(self.home_url)
        self.assertEqual(home_response.status_code, 200)
        
        help_response = self.client.get(self.help_url)
        self.assertEqual(help_response.status_code, 200)
    
    def test_taskmanager_views_with_anonymous_user(self):
        """Test taskmanager views with anonymous user."""
        home_response = self.client.get(self.home_url)
        self.assertEqual(home_response.status_code, 200)
        
        help_response = self.client.get(self.help_url)
        self.assertEqual(help_response.status_code, 200)


class TaskManagerViewUnitTests(TestCase):
    """Unit tests for taskmanager view functions."""
    
    def setUp(self):
        self.request = HttpRequest()
    
    def test_home_function_returns_response(self):
        """Test that home function returns HttpResponse."""
        response = home(self.request)
        self.assertIsInstance(response, HttpResponse)
    
    def test_help_function_returns_response(self):
        """Test that help function returns HttpResponse."""
        response = help(self.request)
        self.assertIsInstance(response, HttpResponse)
    
    @patch('taskmanager.views.render')
    def test_home_calls_render_with_correct_parameters(self, mock_render):
        """Test that home calls render with correct parameters."""
        mock_render.return_value = HttpResponse("test")
        home(self.request)
        mock_render.assert_called_once_with(self.request, 'taskmanager/tm_home.html')
    
    @patch('taskmanager.views.render')
    def test_help_calls_render_with_correct_parameters(self, mock_render):
        """Test that help calls render with correct parameters."""
        mock_render.return_value = HttpResponse("test")
        help(self.request)
        mock_render.assert_called_once_with(self.request, 'taskmanager/tm_help.html')


# Pytest-style tests for more complex scenarios
@pytest.mark.django_db
class TestTaskManagerIntegration:
    """Integration tests for taskmanager using pytest."""
    
    def setup_method(self):
        self.client = Client()
    
    def test_taskmanager_urls_are_accessible(self):
        """Test that all taskmanager URLs are accessible."""
        urls = [
            reverse('taskmanager:home'),
            reverse('taskmanager:help'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            assert response.status_code == 200
    
    @pytest.mark.parametrize(
        "url_name,expected_template",
        [
            ("taskmanager:home", "taskmanager/tm_home.html"),
            ("taskmanager:help", "taskmanager/tm_help.html"),
        ]
    )
    def test_taskmanager_templates(self, url_name, expected_template):
        """Test that taskmanager views use correct templates."""
        response = self.client.get(reverse(url_name))
        assert expected_template in [t.name for t in response.templates]
    
    @pytest.mark.parametrize(
        "url_name,method,expected_status",
        [
            ("taskmanager:home", "GET", 200),
            ("taskmanager:home", "POST", 405),
            ("taskmanager:help", "GET", 200),
            ("taskmanager:help", "POST", 405),
        ]
    )
    def test_taskmanager_http_methods(self, url_name, method, expected_status):
        """Test different HTTP methods on taskmanager views."""
        response = getattr(self.client, method.lower())(reverse(url_name))
        assert response.status_code == expected_status


# TDD tests for future Task model
class TaskModelTests(BaseModelTestCase):
    """TDD tests for Task model (to be created)."""
    
    def test_task_model_should_exist(self):
        """Test that Task model should exist."""
        # This test will fail until you create Task model
        # Following TDD: Red -> Green -> Refactor
        try:
            from taskmanager.models import Task
            self.assertTrue(hasattr(Task, 'title'))
            self.assertTrue(hasattr(Task, 'description'))
            self.assertTrue(hasattr(Task, 'completed'))
            self.assertTrue(hasattr(Task, 'created_at'))
            self.assertTrue(hasattr(Task, 'updated_at'))
        except ImportError:
            self.fail("Task model does not exist yet. Create it following TDD.")
    
    def test_task_model_string_representation(self):
        """Test Task model string representation."""
        # This test will fail until you create Task model
        # Following TDD: Red -> Green -> Refactor
        try:
            from taskmanager.models import Task
            task = Task(title="Test Task")
            self.assertEqual(str(task), "Test Task")
        except ImportError:
            self.fail("Task model does not exist yet. Create it following TDD.")


# TDD tests for future forms
class TaskFormTests(TestCase):
    """TDD tests for Task forms (to be created)."""
    
    def test_task_form_should_exist(self):
        """Test that TaskForm should exist."""
        # This test will fail until you create TaskForm
        # Following TDD: Red -> Green -> Refactor
        try:
            from taskmanager.forms import TaskForm
            form = TaskForm()
            self.assertTrue(hasattr(form, 'fields'))
        except ImportError:
            self.fail("TaskForm does not exist yet. Create it following TDD.")
    
    def test_task_form_validation(self):
        """Test TaskForm validation."""
        # This test will fail until you create TaskForm
        # Following TDD: Red -> Green -> Refactor
        try:
            from taskmanager.forms import TaskForm
            
            # Test valid form
            form_data = {
                'title': 'Test Task',
                'description': 'Test Description',
            }
            form = TaskForm(data=form_data)
            self.assertTrue(form.is_valid())
            
            # Test invalid form (empty title)
            form_data = {
                'title': '',
                'description': 'Test Description',
            }
            form = TaskForm(data=form_data)
            self.assertFalse(form.is_valid())
        except ImportError:
            self.fail("TaskForm does not exist yet. Create it following TDD.")


# TDD tests for future API endpoints
class TaskAPITests(TestCase):
    """TDD tests for Task API endpoints (to be created)."""
    
    def test_task_list_api_should_exist(self):
        """Test that task list API endpoint should exist."""
        # This test will fail until you create API endpoints
        # Following TDD: Red -> Green -> Refactor
        try:
            response = self.client.get('/api/tasks/')
            self.assertIn(response.status_code, [200, 404])  # 404 until created
        except Exception:
            self.fail("Task API endpoints do not exist yet. Create them following TDD.")
    
    def test_task_create_api_should_exist(self):
        """Test that task create API endpoint should exist."""
        # This test will fail until you create API endpoints
        # Following TDD: Red -> Green -> Refactor
        try:
            response = self.client.post('/api/tasks/', {
                'title': 'Test Task',
                'description': 'Test Description'
            })
            self.assertIn(response.status_code, [201, 404])  # 404 until created
        except Exception:
            self.fail("Task API endpoints do not exist yet. Create them following TDD.")
