# taskmanager/tests.py
import pytest
from django.urls import reverse, resolve
from syafiqkaydotcom.utils import get_named_class_based_endpoints
from .models import Task

# helper functions
@pytest.fixture(scope="session")
def django_db_setup():
    return {
        "MIGRATE": True,
    }

# test urls.py
class TestTaskmanagerEndpoints:
    ENDPOINTS = get_named_class_based_endpoints('taskmanager')
    ENDPOINT_URL_NAMES = [name for name, _ in ENDPOINTS]
    
    @pytest.mark.parametrize(
        ("url_name", "expected_class",),
        ENDPOINTS
    )
    def test_view_resolves_to_correct_class(self, url_name, expected_class):
        # URLs that require parameters
        url_kwargs = {}
        if 'detail' in url_name or 'update' in url_name or 'delete' in url_name:
            url_kwargs = {'pk': 1}
        
        resolved = resolve(reverse(url_name, kwargs=url_kwargs))
        assert resolved.func.view_class == expected_class

# test models.py

@pytest.mark.django_db
class TestTaskModel:
    def test_can_create_task(self):
        task = Task(title="New test task")
        assert task is not None
        assert task.title == "New test task"
    
    def test_can_delete_task(self):
        task = Task(title="Task to delete")
        task.save()
        assert Task.objects.filter(id=task.id).exists()
        task.delete()
        assert not Task.objects.filter(id=task.id).exists()
    
    def test_can_update_task(self):
        task = Task(title="Task to update")
        task.save()
        task.title = "Updated task title"
        task.save()
        updated_task = Task.objects.get(id=task.id)
        assert updated_task.title == "Updated task title"
    
    def test_can_view_task(self):
        task = Task(title="Task to view")
        task.save()
        retrieved_task = Task.objects.get(id=task.id)
        assert retrieved_task.title == "Task to view"
    
    @pytest.mark.xfail(reason="linking tasks to sprints not implemented yet")
    def test_can_associate_task_with_sprint(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint 1")
        sprint.save()
        task = Task(title="Task in Sprint 1", sprint=sprint)
        task.save()
        assert task.sprint == sprint
        assert sprint.tasks.filter(id=task.id).exists()
    
    @pytest.mark.xfail(reason="task title validation not implemented yet - need to be written in active speech")
    def test_task_creation_with_invalid_title(self):
        from django.core.exceptions import ValidationError
        task = Task(title="")
        with pytest.raises(ValidationError):
            task.full_clean()
        task.save()
        assert not Task.objects.filter(title="").exists()

    @pytest.mark.xfail(reason="due date validation not implemented yet")
    def test_task_creation_with_invalid_due_date(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        task = Task(title="Task with invalid due date", due_date=timezone.now() - timezone.timedelta(days=1))
        with pytest.raises(ValidationError):
            task.full_clean()
        task.save()
        assert not Task.objects.filter(title="Task with invalid due date").exists()
    
    @pytest.mark.xfail(reason="testing status validation")
    def test_task_creation_with_invalid_status(self):
        from django.core.exceptions import ValidationError
        task = Task(title="Task with invalid status", status="INVALID_STATUS")
        with pytest.raises(ValidationError):
            task.full_clean()
        task.save()
        assert not Task.objects.filter(title="Task with invalid status").exists()
    
    @pytest.mark.xfail(reason="input sanitization not implemented yet")
    def test_task_creation_with_html_in_title(self):
        from django.core.exceptions import ValidationError
        task = Task(title="<script>alert('test')</script>")
        with pytest.raises(ValidationError):
            task.full_clean()
        task.save()
        assert not Task.objects.filter(title="<script>alert('test')</script>").exists()

class TestSprintModel:
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_can_create_sprint(self):
        from .models import Sprint
        sprint = Sprint(name="New Sprint")
        sprint.save()
        assert sprint is not None
        assert sprint.name == "New Sprint"
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_can_delete_sprint(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint to delete")
        sprint.save()
        assert Sprint.objects.filter(id=sprint.id).exists()
        sprint.delete()
        assert not Sprint.objects.filter(id=sprint.id).exists()
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_can_update_sprint(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint to update")
        sprint.save()
        sprint.name = "Updated Sprint Name"
        sprint.save()
        updated_sprint = Sprint.objects.get(id=sprint.id)
        assert updated_sprint.name == "Updated Sprint Name"
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_can_view_sprint(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint to view")
        sprint.save()
        retrieved_sprint = Sprint.objects.get(id=sprint.id)
        assert retrieved_sprint.name == "Sprint to view"
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_can_associate_sprint_with_tasks(self):
        from .models import Sprint, Task
        sprint = Sprint(name="Sprint with Tasks")
        sprint.save()
        task1 = Task(title="Task 1 in Sprint")
        task1.save()
        task2 = Task(title="Task 2 in Sprint")
        task2.save()
        sprint.tasks.add(task1, task2)
        assert sprint.tasks.count() == 2
        assert task1.sprints.filter(id=sprint.id).exists()
        assert task2.sprints.filter(id=sprint.id).exists()

    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_sprint_end_date_after_start_date(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint with valid dates", start_date="2023-01-01", end_date="2023-01-10")
        sprint.full_clean()
        sprint.save()
        assert Sprint.objects.filter(name="Sprint with valid dates").exists()
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_sprint_end_date_before_start_date(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint with invalid dates", start_date="2023-01-10", end_date="2023-01-01")
        with pytest.raises(Exception):
            sprint.full_clean()
        sprint.save()
        assert not Sprint.objects.filter(name="Sprint with invalid dates").exists()
        return "Epic model for task management, grouping related tasks into larger bodies of work."
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_sprint_creator(self):
        from django.contrib.auth.models import User
        from .models import Sprint
        user = User.objects.create_user(username='testuser', password='testpass')
        sprint = Sprint(name="Sprint with Creator", creator=user)
        sprint.save()
        assert sprint.creator == user
        assert user.created_sprints.filter(id=sprint.id).exists()
    
    @pytest.mark.xfail(reason="still building the Sprint model")
    def test_sprint_description(self):
        from .models import Sprint
        sprint = Sprint(name="Sprint with Description", description="This is a test sprint.")
        sprint.save()
        assert sprint.description == "This is a test sprint."
        retrieved_sprint = Sprint.objects.get(id=sprint.id)
        assert retrieved_sprint.description == "This is a test sprint."
    
    
@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestEpicModel:
    pass

# test views.py
@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestTaskView:
    pass

@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestSprintView:
    pass

@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestEpicView:
    pass    

# test services.py
@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestTaskService:
    pass

@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestSprintService:
    pass

@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestEpicService:
    pass

# test integration
@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestTaskManagerIntegration:
    pass

# test function
@pytest.mark.xfail(reason="Models tests are not implemented yet")
class TestTaskManagerFunctional:
    pass