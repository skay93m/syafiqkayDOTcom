# tests/factories.py
"""
Factory classes for creating test data.
Used in Test-Driven Development to create consistent test objects.
"""
import factory
from django.contrib.auth.models import User
from django.utils import timezone
from taskmanager.models import Task


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances in tests."""
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False
    date_joined = factory.LazyFunction(timezone.now)


class SuperUserFactory(UserFactory):
    """Factory for creating superuser instances in tests."""
    
    is_staff = True
    is_superuser = True
    username = factory.Sequence(lambda n: f'admin{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for creating Task instances in tests."""
    
    class Meta:
        model = Task
        django_get_or_create = ('title',)
    
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    completed = False
    user = factory.SubFactory(UserFactory)
