from django.contrib import admin
from .models import MovieList, Movie, DiscussionPost, Comment, Profile
# Register your models here.

admin.site.register(MovieList)
admin.site.register(Movie)
admin.site.register(DiscussionPost)
admin.site.register(Comment)
admin.site.register(Profile)