from django.urls import path, include

from application.urls import urlpatterns as application

urlpatterns = [
    path('application/', include((application, 'application'), namespace='application'))
]
