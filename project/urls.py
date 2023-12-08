from django.urls import path

from project.views import *

urlpatterns = [
    path('project/', ProjectView.as_view()),
    path('project-create/', ProjectCreateView.as_view()),
]
