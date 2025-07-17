from django.urls import path
from django.views.generic import TemplateView
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    SprintCreateView,
    SprintUpdateView,
    SprintDeleteView,
    SprintDetailView,
    SprintListView,
    SprintTaskListView,
    EpicCreateView,
    EpicUpdateView,
    EpicDeleteView,
    EpicDetailView,
    EpicListView,
    custom_404,
    custom_500,
)
)


app_name = 'taskmanager'
urlpatterns = [
    # Home and Help Pages
    path('', TemplateView.as_view(template_name="taskmanager/taskmanager.html"), name='home'),
    path('help/', TemplateView.as_view(template_name="taskmanager/help.html"), name='help'),
    
    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task-list'), # GET
    path('tasks/new/', TaskCreateView.as_view(), name='task-create'), # GET, POST
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'), # GET
    path(
        'tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'), # GET/POST
    path(
        'tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'), # POST
    path('tasks/sprint/add_task/<int:pk>/', create_task_on_sprint, name='task-add-to-sprint'),
    
    # Sprint URLs
    path('sprints/new/', SprintCreateView.as_view(), name='sprint-create'),
    path('sprints/<int:pk>/edit/', SprintUpdateView.as_view(), name='sprint-update'),
    path('sprints/<int:pk>/delete/', SprintDeleteView.as_view(), name='sprint-delete'),
    path('sprints/<int:pk>/', SprintDetailView.as_view(), name='sprint-detail'),
    path('sprints/', SprintListView.as_view(), name='sprint-list'),
    path('sprints/<int:pk>/tasks/', SprintTaskListView.as_view(), name='sprint-task-list'),
    
    # Epic URLs
    path('epics/new/', EpicCreateView.as_view(), name='epic-create'),
    path('epics/<int:pk>/edit/', EpicUpdateView.as_view(), name='epic-update'),
    path('epics/<int:pk>/delete/', EpicDeleteView.as_view(), name='epic-delete'),
    path('epics/<int:pk>/', EpicDetailView.as_view(), name='epic-detail'),
    # Error Handling
    # The following error handlers are set below, not as URL patterns.
    
    # Trigger Error for Testing
    # Uncomment the next line to enable the error trigger endpoint
    # path('trigger-error/', trigger_error, name='trigger-error'),
    # Trigger Error for Testing
    # Uncomment the next line to enable the error trigger endpoint
    # from .views import trigger_error
    # path('trigger-error/', trigger_error, name='trigger-error'),

handler404 = 'taskmanager.views.custom_404'
handler500 = 'taskmanager.views.custom_500'