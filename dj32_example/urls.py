from django.urls import path, include

from application.urls import urlpatterns as application
from project.urls import urlpatterns as project
from users.urls import urlpatterns as users

urlpatterns = [
    path('application/', include((application, 'application'), namespace='application')),
    path('project/', include((project, 'project'), namespace='project')),
    path('users/', include((users, 'users'), namespace='users'))
]
