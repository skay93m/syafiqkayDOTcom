# taskmanager/urls.py
from django.urls import path
from .views import (
    ViewTaskManagerHomepage,
    ViewTaskManagerHelpPage,
    ViewTaskList,
    ViewTaskCreate,
    ViewTaskDetail,
)

app_name = 'taskmanager'
urlpatterns = [
    # Home and Help Pages
    path('', ViewTaskManagerHomepage.as_view(), name='task-manager-homepage'),
    path('help/', ViewTaskManagerHelpPage.as_view(), name='task-manager-help-page'),
    # Tasks pages
    path('task/list/', ViewTaskList.as_view(), name='task-list'),
    path('task/new/', ViewTaskCreate.as_view(), name='task-create'),
    path('task/detail/<int:pk>/', ViewTaskDetail.as_view(), name='task-detail'),
    # Sprints pages
    # Epic pages
]