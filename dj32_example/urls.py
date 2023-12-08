from django.urls import path, include

from application.urls import urlpatterns as application
from project.urls import urlpatterns as project

urlpatterns = [
    path('application/', include((application, 'application'), namespace='application')),
    path('project/', include((project, 'project'), namespace='project'))
]
