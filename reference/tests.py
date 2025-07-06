from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Reference


class ReferenceModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_reference_creation(self):
        reference = Reference.objects.create(
            title='Test Reference',
            summary='Test summary',
            content='Test content',
            author=self.user
        )
        self.assertEqual(reference.title, 'Test Reference')
        self.assertEqual(str(reference), 'Test Reference')
        
    def test_reference_absolute_url(self):
        reference = Reference.objects.create(
            title='Test Reference',
            content='Test content',
            author=self.user
        )
        expected_url = f'/reference/{reference.id}/'
        self.assertEqual(reference.get_absolute_url(), expected_url)
