# taskmanager/tests.py
import pytest
from django.urls import reverse, resolve
from syafiqkaydotcom.utils import get_named_class_based_endpoints
from .models import Task

# some helper functions
@pytest.fixture(scope="session")
def django_db_setup():
    return {
        "MIGRATE": True,
    }

# test urls.py
class TestTaskmanagerEndpoints:
    ENDPOINTS = get_named_class_based_endpoints('taskmanager')
    ENDPOINT_URL_NAMES = [name for name, _ in ENDPOINTS]
    
    @pytest.mark.parametrize("url_name, expected_class", ENDPOINTS)
    def test_view_resolves_to_correct_class(self, url_name, expected_class):
        resolved = resolve(reverse(url_name))
        assert resolved.func.view_class == expected_class

# test models.py
class TestTaskModel:
    def test_can_create_task(self):
        task = Task(title="New test task")
        assert task is not None
        assert task.title == "New test task"
    
    @pytest.mark.django_db
    def test_can_delete_task(self):
        task = Task(title="Task to delete")
        task.save()
        task_id = task.id
        task.delete()
        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(id=task_id)
    
# class TestSprintModel:

# class TestEpicModel:

# test views.py
# class TestTaskView:

# class TestSprintView:
    
# class TestEpicView:
    
# test services.py
# class TestTaskService:
    
# class TestSprintService:

# class TestEpicService:

# test integration
# class TestTaskManagerIntegration:

# test function
# class TestTaskManagerFunctional:
