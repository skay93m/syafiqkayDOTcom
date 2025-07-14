from django.urls import path
from .views import homepage
app_name = "homepage" # This is the namespace for the homepage app
urlpatterns = [
    path('', homepage, name='homepage'),  # Maps the root URL to the homepage view
]