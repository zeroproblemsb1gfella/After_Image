# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('<str:name>', views.month, name='month'),
    path('<str:name>/<str:title>', views.movie, name = "movie"),
    path("", views.home, name = "home")
]   