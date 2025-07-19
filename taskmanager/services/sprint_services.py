# taskmanager/services/sprint_services.py

from datetime import datetime

from django.core.exceptions import ValidationError

from ..models import Sprint, Epic, Task, User

def create_sprint(
    name: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    user: User
) -> Sprint:
    """
    Create a new Sprint object with validation.
    """
    if start_date >= end_date:
        raise ValidationError("Start date must be before end date.")
    
    sprint = Sprint(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        creator=user
    )

    sprint.save()
    
    return sprint

def remove_task_from_sprint(
    sprint: Sprint, 
    task: Task
) -> Sprint:
    """
    Remove a task from a sprint.
    """
    sprint.tasks.remove(task)
    return sprint

def set_sprint_epic(
    sprint: Sprint, 
    epic: Epic
) -> Sprint:
    """
    Set the epic for the sprint.
    """
    sprint.epic = epic
    return sprint