# syafiqkaydotcom/homepage/urls.py

from django.urls import path
from homepage.views import ViewHomepage, ViewCV

app_name = "homepage" 

urlpatterns = [
    # homepage
    path('', ViewHomepage.as_view(), name='homepage'),
    # cv
    path('cv/', ViewCV.as_view(), name='cv')
    # path ('cv/employment/', ViewEmployment.as_view(), name='employment-list')
    # path ('cv/education/', ViewEducation.as_view(), name='education-list')
    # path ('cv/skills/', ViewSkills.as_view(), name='skills-list')
    # path ('cv/credentials/', ViewCredentials.as_view(), name='credentials-list')
]