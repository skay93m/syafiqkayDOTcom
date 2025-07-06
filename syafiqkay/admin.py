from django.contrib import admin

# Customize the admin site
admin.site.site_header = "Syafiq Kay Admin 🌸"
admin.site.site_title = "Syafiq Kay Admin Portal"
admin.site.index_title = "Welcome to Syafiq Kay Admin Portal"

# Custom admin CSS
class AdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        context['index_title'] = self.index_title
        return context

# Override the default admin site
admin.site.__class__ = AdminSite
