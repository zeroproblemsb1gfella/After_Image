from django.contrib import admin
from .models import MovieList, Movie, DiscussionPost, Comment, MyUser, Discussion_Likes, Movie_Watched
# Register your models here.

admin.site.register(MyUser)
admin.site.register(MovieList)
admin.site.register(Movie)
admin.site.register(DiscussionPost)
admin.site.register(Comment)
admin.site.register(Discussion_Likes)
admin.site.register(Movie_Watched)