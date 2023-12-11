from django.urls import path

from users.views import *

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('user-login/', UsersLoginView.as_view()),
]
