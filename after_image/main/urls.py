# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import go_back

urlpatterns = [
    path('go-back/', go_back, name='go_back'),
    path('movie/<str:name>', views.month, name='month'),
    path('movie/<str:name>/<str:title>', views.movie, name = "movie"),
    path('movie/<str:name>/<str:title>/discussionposts', views.discussionposts, name = 'discussionposts'),
    path('movie/<str:name>/<str:title>/discussionposts/<int:id>', views.discussionpost, name = 'discussionpost'),
    path("", views.initial_register_or_login, name = "initial_register_or_login"),
    path("home", views.home, name = "home"),
    path("initial_register_or_login", views.initial_register_or_login, name = "initial_register_or_login"),
    path("popular", views.popular, name = "popular"),
    path("profile", views.profile, name = "profile"),
    path("about", views.about, name = "about"),
    path('movie/<str:name>/<str:title>/toggle_watched', views.toggle_watched, name = "toggle_watched"),
    path('movie/<str:name>/<str:title>/discussionposts/<int:id>/toggle_likes', views.toggle_likes, name = "toggle_likes")
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)