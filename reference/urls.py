from django.urls import path
from . import views

app_name = "reference"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.reference_detail, name='reference_detail'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('api/categories/', views.get_all_categories, name='get_all_categories'),
]
