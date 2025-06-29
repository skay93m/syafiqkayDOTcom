from django.urls import path
from . import views

app_name = "journals"

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
]