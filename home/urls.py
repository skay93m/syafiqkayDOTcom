from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('testing-guide/', views.testing_guide, name='testing_guide'),
]
