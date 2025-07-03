from django.urls import path
from . import views

app_name = "journals"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('trigger-400/', views.trigger_400, name='trigger_400'),
    path('trigger-403/', views.trigger_403, name='trigger_403'),
    path('trigger-404/', views.trigger_404, name='trigger_404'),
    path('trigger-500/', views.trigger_500, name='trigger_500'),
]