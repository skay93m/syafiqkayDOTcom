"""
URL configuration for syafiqkay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import error_handlers

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("journals/", include("journals.urls")),
    path("noto_garden/", include("noto_garden.urls")),
<<<<<<< HEAD
    path("reference/", include("reference.urls")),
    path("experiments/", include("experiments.urls")),
    # Favicon handling
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
    # Error testing URLs
    path("test-401/", error_handlers.custom_401, name="test_401"),
    path("test-402/", error_handlers.custom_402, name="test_402"),
    path("test-405/", error_handlers.custom_405, name="test_405"),
    path("test-406/", error_handlers.custom_406, name="test_406"),
    path("test-407/", error_handlers.custom_407, name="test_407"),
    path("test-408/", error_handlers.custom_408, name="test_408"),
    path("test-409/", error_handlers.custom_409, name="test_409"),
    path("test-410/", error_handlers.custom_410, name="test_410"),
    path("test-501/", error_handlers.custom_501, name="test_501"),
    path("test-502/", error_handlers.custom_502, name="test_502"),
    path("test-503/", error_handlers.custom_503, name="test_503"),
    path("test-504/", error_handlers.custom_504, name="test_504"),
    path("test-505/", error_handlers.custom_505, name="test_505"),
=======
>>>>>>> 1b750c1 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
]

# Add static files serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers (for production)
handler404 = error_handlers.custom_404
handler500 = error_handlers.custom_500
