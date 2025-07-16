# taskmanager/services.py
from django.shortcuts import get_object_or_404
from .models import Sprint, Task, User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models, transaction
from django.core.exceptions import ValidationError

def can_add_task_to_sprint(task, sprint_id):
    """
    Check if a task can be added to a sprint based on the sprint's date range.
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return sprint.start_date <= task.created_at.date() <= sprint.end_date

def check_task(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Extract the 'task_id' parameter from the POST data
        task_id = request.POST.get('task_id')
        if services.check_task(task_id):
            return HttpResponseRedirect(reverse("success"))
        if task_id:
            return HttpResponseRedirect(reverse("success"))
        else:
            # If no ID was provided, re-render the form with an error message
            return render(
                request, 
                'taskmanager/add_task_to_sprint.html', 
                {'error': 'Task ID is required.'}
            )
    else:
        # If the request method is not POST, render the form
        return render(request, 'taskmanager/check_task.html')
    
def create_task_and_add_to_sprint(
    task_data: dict[str, str],
    sprint_id: int,
    creator: User
) -> Task:
    """
    Create a new task and add it to the specified sprint.
    """
    
    # Fetch the sprint by its ID
    sprint = Sprint.objects.get(id=sprint_id)
    
    # Get the current date and time
    now = datetime.now()
    
    # Check if the current date and time is within the sprint's date range
    if not (sprint.start_date <= now.date() <= sprint.end_date):
        raise ValidationError("Cannot add task to sprint: Current date is not within the sprint's start and end dates.")
    with transaction.atomic():
        # Create the task with the provided data
        task = Task.objects.create(
            title=task_data['title'],
            description=task_dataget('description', ''),
            status=task_data.get('status', 'UNASSIGNED'),
            creator=creator,
        )
        # Add the task to the sprint
        sprint.tasks.add(task)
    return task

class TaskAlreadyClaimedException(Exception):
    pass

@transaction.atomic
def claim_task(user_id: int, task_id: int) -> None:
    # Lock the task row to prevent other transactions from claiming it simultaneously
    task = Task.objects.select_for_update().get(id=task_id)
    # Check if the task is already claimed or completed
    if task.owner_id:
        raise TaskAlreadyClaimedException("Task is already claimed or completed.")
    # Claim the task
    task.status = "IN_PROGRESS"
    task.owner_id = user_id
    task.save()