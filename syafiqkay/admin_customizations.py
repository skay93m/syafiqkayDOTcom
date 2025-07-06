from django.contrib import admin


def setup_admin():
    """Setup admin customizations after Django is ready."""
    # Customize the admin site
    admin.site.site_header = "Syafiq Kay Admin 🌸"
    admin.site.site_title = "Syafiq Kay Admin Portal"
    admin.site.index_title = "Welcome to Syafiq Kay Admin Portal"
