from django.urls import path
from . import views

app_name = 'taskmanager'
urlpatterns = [
    path('', views.home, name='home'),
    path('help/', views.help, name='help'),
]
