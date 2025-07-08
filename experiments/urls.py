from django.urls import path
from . import views

app_name = 'experiments'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('detail/<slug:slug>/', views.experiment_detail, name='detail'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),  # Keep for reference
]
