# taskmanager/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .services.models_services import VersionMixing


# task
class Task(models.Model):
    '''
    Task model for task management.
    A Task is a single unit of work that needs to be completed.
    It can be assigned to a user and has a status.
    '''
    STATUS_CHOICES = [
        ("UNASSIGNED", "Unassigned"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Completed"),
        ("ARCHIVED", "Archived"),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False, default="")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="UNASSIGNED", 
        db_comment="Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED.",
    )
    due_date = models.DateField(
        default=timezone.now,
        db_comment="The date by which the task should be completed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User,
        null=True,
        related_name="created_tasks", 
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User, 
        related_name="owned_tasks", 
        on_delete=models.SET_NULL, 
        null=True, 
        db_comment="Foreign Key to the User who currently owns the task.",
    )
    epic = models.ForeignKey(
        'Epic',
        related_name="tasks",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_comment="Foreign Key to the Epic this task belongs to."
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table_comment = "Holds information about tasks"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status='UNASSIGNED')|
                models.Q(status='IN_PROGRESS')|
                models.Q(status='DONE')|
                models.Q(status='ARCHIVED'),
                name='status_check'
            ),
            models.CheckConstraint(
                check=models.Q(
                    due_date__gte=models.functions.Cast(
                        models.F('created_at'),
                        output_field=models.DateField()
                    )
                ),
                name='due_date_not_before_created_date'
            ),
        ]
    
# sprint
class Sprint(models.Model):
    '''
    Sprint model for task management.
    A Sprint is a time-boxed period during which a specific set of tasks are completed.
    It is used to manage the progress of tasks in an agile development process.
    '''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, 
        related_name='created_sprints', 
        on_delete=models.CASCADE
    )
    tasks = models.ManyToManyField(
        Task,
        related_name='sprints',
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        db_table_comment = "holds Sprint information"
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')), 
                name='end_date_after_start_date'
            ),
        ]

# epic
class Epic(models.Model):
    '''
    Epic model for task management.
    An Epic is a large body of work that can be broken down into smaller tasks.
    It is used to group related tasks together.
    '''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, 
        null=True,
        related_name='created_epics', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table_comment = "holds Epic information"