# syafiqkaydotcom/utils.py

from django.urls import get_resolver
from django.views.generic import View

def assert_response_ok(response, url_name):
    assert response.status_code == 200, (
        f"❌ Response for '{url_name}' failed with status code {response.status_code}\n"
        f"▶ URL: {response.request.META['PATH_INFO']}\n"
        f"▶ Reason: {response.reason_phrase}\n"
        f"▶ Body:\n{response.content.decode('utf-8')[:1000]}"  # Limit length for console readability
    )

from django.urls import get_resolver, URLPattern, URLResolver
from django.views import View

def get_named_class_based_endpoints(app_namespace=None):
    endpoints = []

    def extract_patterns(urlpatterns, namespace=None):
        for pattern in urlpatterns:
            if isinstance(pattern, URLPattern):  # Single route
                full_name = f"{namespace}:{pattern.name}" if namespace and pattern.name else pattern.name
                view_class = getattr(pattern.callback, 'view_class', None)
                if pattern.name and view_class and issubclass(view_class, View):
                    endpoints.append((full_name, view_class))
            elif isinstance(pattern, URLResolver):  # Include()d patterns
                sub_namespace = pattern.namespace or namespace
                extract_patterns(pattern.url_patterns, sub_namespace)

    extract_patterns(get_resolver().url_patterns)
    if app_namespace:
        endpoints = [ep for ep in endpoints if ep[0].startswith(f"{app_namespace}:")]
    return endpoints

