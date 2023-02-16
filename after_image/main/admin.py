from django.contrib import admin
from .models import MovieList, Movie, DiscussionPost, Comment
# Register your models here.

admin.site.register(MovieList)
admin.site.register(Movie)
admin.site.register(DiscussionPost)
admin.site.register(Comment)