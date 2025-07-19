# homepage/homepage_views.py
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from syafiqkaydotcom.decorators import ensure_200_status

'''
Homepage
'''

@method_decorator(ensure_200_status, name='get')
class ViewHomepage(TemplateView):
    template_name = 'homepage/homepage.html'

'''
CV
'''

@method_decorator(ensure_200_status, name='get')
class ViewCV(TemplateView):
    template_name = 'cv/cv_dashboard.html'