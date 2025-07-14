from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', 'homepage')),
    path('taskmanager/', include('taskmanager.urls', 'taskmanager')),
]
