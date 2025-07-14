from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

app_name = 'taskmanager'

urlpatterns = [
    path('', TemplateView.as_view(template_name='taskmanager/home.html'), name="home"),
    path('help/', TemplateView.as_view(template_name='taskmanager/help.html'), name='help'),
]
