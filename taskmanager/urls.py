# taskmanager/urls.py
from django.urls import path
from .views import (
    ViewTaskManagerHomepage,
    ViewTaskManagerHelpPage,
)

app_name = 'taskmanager'
urlpatterns = [
    # Home and Help Pages
    path('', ViewTaskManagerHomepage.as_view(), name='task-manager-homepage'),
    path('help/', ViewTaskManagerHelpPage.as_view(), name='task-manager-help-page'),
    # Tasks pages
    # Sprints pages
    # Epic pages
]