from django.urls import path
from . import views

app_name = "notoGarden"

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
]