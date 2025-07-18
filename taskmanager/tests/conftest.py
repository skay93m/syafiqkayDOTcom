# conftest.py

'''
Best Practices
- Keep fixtures atomic: one purpose per fixture
- Use composition: build complex fixtures from simpler ones
- Use scope='function' (default) unless you need session-wide setup
- Place them in conftest.py for global access, or in test_*.py for local use
'''

'''
Pytest fixtures can be scoped to control how often they are created and reused.
The default scope is 'function', which means the fixture is re-created for every test.

Available scopes:
1. function  → (default) Creates a fresh fixture for each test function. Use for most cases to ensure test isolation.

2. class     → Shared across all tests in a single test class. Use when setup is expensive and reused within a class.

3. module    → Shared across all tests in a single test module (file). Use when setup is reused across multiple functions in one file.

4. session   → Shared across the entire test session (all files). Use for global setup like database connections or config loading.

5. package   → Shared across all tests in a package (directory). Use for package-wide setup that is reused across multiple modules.

6. global    → Shared across all tests in the entire project. Use for project-wide setup that is reused across multiple packages.

7. autouse   → Automatically applies to all tests without explicit request. Use for setup that should always run, like logging or test environment config.

8. once      → Runs only once per test session, regardless of scope. Use for expensive setup that doesn't need to be repeated, like database migrations.

9. shared    → Similar to 'once', but can be shared across multiple test runs. Use for shared resources that can be reused across multiple test sessions.

10. transient → Creates a fresh fixture for each test, but can be reused within the same test function. Use for setup that needs to be isolated but can be reused within a single test.

11. persistent → Similar to 'shared', but persists across multiple test sessions. Use for setup that needs to be reused across multiple test sessions.

Be cautious with broader scopes — they can lead to test coupling or stale state.

'''

import pytest
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Core fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='password123',
    )

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='password123')
    return client

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        password='adminpassword',
    )

@pytest.fixture
def anonymous_client(client):
    return client

# Model fixtures
'''
sample_task
sample_sprint
sample_epic
task_with_sprint
task_with_epic
sprint_with_tasks
epic_with_tasks
'''

# Relationship fixtures

# Permission and ownership fixtures

# Utility fixtures