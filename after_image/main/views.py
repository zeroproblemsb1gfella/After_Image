from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import MovieList, Movie

def month(response, name):
    ls = MovieList.objects.get(name = name)
    return render(response, "main/month.html", {"ls":ls})

def movie(response, name, title):
    ls = MovieList.objects.all().get(name = name)
    movie = ls.movie_set.get(title = title)
    return render(response, "main/movie.html",{"movie":movie})

def home(response):
    ls = MovieList.objects.all()
    return render(response, "main/home.html", {"ls":ls})