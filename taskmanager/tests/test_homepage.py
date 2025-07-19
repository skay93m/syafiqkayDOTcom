# taskmanager/tests/test_homepage.py
from django.test import TestCase
from django.urls import reverse

class HomepageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('taskmanager:home'))
        self.assertEqual(response.status_code, 200)