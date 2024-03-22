from django.urls import path, include

from project.urls import urlpatterns as project
from users.urls import urlpatterns as users

urlpatterns = [
    path("project/", include((project, "project"), namespace="project")),
    path("users/", include((users, "users"), namespace="users")),
]
