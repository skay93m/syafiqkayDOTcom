from django.urls import path
from django.views.generic import TemplateView
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    create_task_on_sprint
)

app_name = 'taskmanager'
urlpatterns = [
    path('', TemplateView.as_view(template_name="taskmanager/taskmanager.html"), name='home'),
    path('help/', TemplateView.as_view(template_name="taskmanager/help.html"), name='help'),
    path('tasks/', TaskListView.as_view(), name='task-list'), # GET
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'), # POST
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'), # GET
    path(
        'tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'), # PUT/PATCH
    path(
        'tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/sprint/add_task/<int:pk>/', create_task_on_sprint, name='task-add-to-sprint'),
]
