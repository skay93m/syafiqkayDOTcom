from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string

class HomeViewTests(TestCase):
    def setUp(self):
        """Set up test client and common test data"""
        self.client = Client()
        
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_uses_correct_template(self):
        """Test that home page uses the correct template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/index.html')
    
    def test_home_page_contains_expected_content(self):
        """Test that home page contains expected HTML content"""
        response = self.client.get('/')
        
        # Check for specific HTML elements
        self.assertContains(response, '<h1>Welcome to My Site</h1>')
        self.assertContains(response, 'Hello, Visitor!')
        self.assertContains(response, 'Welcome to our website!')
        self.assertContains(response, 'This is a test template.')
    
    def test_home_page_context_variables(self):
        """Test that the correct context variables are passed to template"""
        response = self.client.get('/')
        
        # Check context variables
        self.assertEqual(response.context['page_title'], 'Home Page')
        self.assertEqual(response.context['user_name'], 'Visitor')
        self.assertEqual(response.context['message'], 'Welcome to our website!')
    
    def test_home_page_title_in_head(self):
        """Test that page title appears in HTML head"""
        response = self.client.get('/')
        self.assertContains(response, '<title>Home Page</title>')
    
    def test_template_renders_with_custom_context(self):
        """Test template rendering with custom context data"""
        # Test the template directly with custom context
        context = {
            'page_title': 'Custom Title',
            'user_name': 'John Doe',
            'message': 'Custom message'
        }
        
        rendered = render_to_string('home/index.html', context)
        
        # Check that custom context is rendered
        self.assertIn('Custom Title', rendered)
        self.assertIn('Hello, John Doe!', rendered)
        self.assertIn('Custom message', rendered)
    
    def test_template_conditional_rendering(self):
        """Test template conditional rendering (when message is None)"""
        context = {
            'page_title': 'Test',
            'user_name': 'Test User',
            'message': None  # No message
        }
        
        rendered = render_to_string('home/index.html', context)
        
        # Should not contain the message paragraph when message is None
        self.assertNotIn('<p class="message">', rendered)
        self.assertIn('Hello, Test User!', rendered)

class TemplateTagTests(TestCase):
    """Test Django template tags and filters"""
    
    def test_template_with_conditional_blocks(self):
        """Test template conditional blocks work correctly"""
        # Test with message present
        context_with_message = {
            'page_title': 'Test',
            'user_name': 'User',
            'message': 'Test message'
        }
        
        rendered = render_to_string('home/index.html', context_with_message)
        self.assertIn('class="message"', rendered)
        self.assertIn('Test message', rendered)
        
        # Test without message
        context_without_message = {
            'page_title': 'Test',
            'user_name': 'User',
            'message': ''
        }
        
        rendered = render_to_string('home/index.html', context_without_message)
        self.assertNotIn('class="message"', rendered)
