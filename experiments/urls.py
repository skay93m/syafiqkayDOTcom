from django.urls import path
from . import views

app_name = 'experiments'

urlpatterns = [
    path('', views.coming_soon, name='dashboard'),  # Temporary coming soon
    path('detail/<slug:slug>/', views.experiment_detail, name='detail'),
]
