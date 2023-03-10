# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('movie/<str:name>', views.month, name='month'),
    path('movie/<str:name>/<str:title>', views.movie, name = "movie"),
    path('movie/<str:name>/<str:title>/discussionposts', views.discussionposts, name = 'discussionposts'),
    path('movie/<str:name>/<str:title>/discussionposts/<int:id>', views.discussionpost, name = 'discussionpost'),
    path("", views.initial_register_or_login, name = "initial_register_or_login"),
    path("home", views.home, name = "home"),
    path("vote", views.vote, name = "vote"),
    path("initial_register_or_login", views.initial_register_or_login, name = "initial_register_or_login"),
    path("popular", views.popular, name = "popular"),
    path("timeline", views.timeline, name = "timeline"),
    path("profile", views.profile, name = "profile"),
    path("about", views.about, name = "about")
]   