# taskmanager/urls.py
from django.urls import path
from .views import (
    ViewTaskManagerHomepage,
    ViewTaskManagerHelpPage,
    ViewTaskList,
    ViewTaskCreate,
    ViewTaskDetail,
    ViewTaskDelete,
    ViewTaskUpdate,
    ViewSprintList,
    ViewSprintDetail,
    ViewSprintCreate,
)

app_name = 'taskmanager'
urlpatterns = [
    # Home and Help Pages
    path('', ViewTaskManagerHomepage.as_view(), name='task-manager-homepage'),
    path('help/', ViewTaskManagerHelpPage.as_view(), name='task-manager-help-page'),
    # Tasks pages
    path('task/list/', ViewTaskList.as_view(), name='task-list'),
    path('task/new/', ViewTaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/', ViewTaskDetail.as_view(), name='task-detail'),
    path('task/<int:pk>/delete/', ViewTaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/update/', ViewTaskUpdate.as_view(), name='task-update'),
    # Sprints pages
    path('sprint/list/', ViewSprintList.as_view(), name='sprint-list'),
    path('sprint/<int:pk>/', ViewSprintDetail.as_view(), name='sprint-detail'),
    path('sprint/new/', ViewSprintCreate.as_view(), name='sprint-create'),
    # Epic pages
]