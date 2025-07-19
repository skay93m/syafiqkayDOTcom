from django.urls import path
from .views.views import HomePageView, HelpPageView

app_name = 'taskmanager'
urlpatterns = [
    # Home and Help Pages
    path('', HomePageView.as_view(), name='home'),
    path('help/', HelpPageView.as_view(), name='help'),
]