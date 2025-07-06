from django.urls import path
from .views import homepage, security_assessment, session_summary

app_name = "homepage"
urlpatterns = [
    path("", homepage, name="homepage"),
    path("security-assessment/", security_assessment, name="security_assessment"),
    path("session-summary/", session_summary, name="session_summary"),
]