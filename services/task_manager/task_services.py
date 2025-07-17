# taskmanager/services/task_services.py

# Standard library imports
from datetime import datetime
from typing import Dict

# Django imports
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Third-party imports
from rest_framework import status

# Local imports
from ...taskmanager.models import Sprint, Task

def claim_task_view(request, task_id):
    user_id = request.user.id
    try:
        claim_task(user_id, task_id)
        return JsonResponse({'message': 'Task claimed successfully'})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist", status=status.HTTP_404_NOT_FOUND)
    except TaskAlreadyClaimedException:
        return HttpResponse("Task already claimed or completed", status=status.HTTP_400_BAD_REQUEST)

def create_task_on_sprint(request: HttpRequest, sprint_id: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        task_data: Dict[str, str] = {
            'title': request.POST.get('title', ''),
            'description': request.POST.get('description', ''),
            'status': request.POST.get('status', 'UNASSIGNED'),
        }
        task = create_task_and_add_to_sprint(task_data, sprint_id, request.user)
        return redirect('taskmanager:task-detail', pk=task.id)
    raise Http404("Not found")

def can_add_task_to_sprint(task, sprint_id):
    """
    Check if a task can be added to a sprint based on the sprint's date range.
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return sprint.start_date <= task.created_at.date() <= sprint.end_date
    
def create_task_and_add_to_sprint(
    task_data: Dict[str, str],
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
            description=task_data.get('description', ''),
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
    if task.owner_id or task.status == "COMPLETED":
        raise TaskAlreadyClaimedException("Task is already claimed or completed.")
    # Claim the task
    task.status = "IN_PROGRESS"
    task.owner_id = user_id
    task.save()