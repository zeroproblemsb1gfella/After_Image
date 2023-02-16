# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('<str:name>', views.month, name='month'),
    path('<str:name>/<str:title>', views.movie, name = "movie"),
    path('<str:name>/<str:title>/discussionposts', views.discussionposts, name = 'discussionposts'),
    path('<str:name>/<str:title>/discussionposts/<int:id>', views.discussionpost, name = 'discussionpost'),
    path("", views.home, name = "home")
]   