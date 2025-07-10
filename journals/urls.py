from django.urls import path
from . import views

app_name = "journals"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('trigger-400/', views.trigger_400, name='trigger_400'),
    path('trigger-401/', views.trigger_401, name='trigger_401'),
    path('trigger-402/', views.trigger_402, name='trigger_402'),
    path('trigger-403/', views.trigger_403, name='trigger_403'),
    path('trigger-404/', views.trigger_404, name='trigger_404'),
    path('trigger-405/', views.trigger_405, name='trigger_405'),
    path('trigger-406/', views.trigger_406, name='trigger_406'),
    path('trigger-407/', views.trigger_407, name='trigger_407'),
    path('trigger-408/', views.trigger_408, name='trigger_408'),
    path('trigger-409/', views.trigger_409, name='trigger_409'),
    path('trigger-410/', views.trigger_410, name='trigger_410'),
    path('trigger-500/', views.trigger_500, name='trigger_500'),
    path('trigger-501/', views.trigger_501, name='trigger_501'),
    path('trigger-502/', views.trigger_502, name='trigger_502'),
    path('trigger-503/', views.trigger_503, name='trigger_503'),
    path('trigger-504/', views.trigger_504, name='trigger_504'),
    path('trigger-505/', views.trigger_505, name='trigger_505'),
]