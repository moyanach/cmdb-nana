from django.urls import path

from application.views import *

urlpatterns = [
    path('application/base/', ApplicationBaseView.as_view()),
    path('application/base/<str:_id>/', ApplicationSingleView.as_view()),
]
