from django.shortcuts import render
from .forms import CreateNewDiscussionPost, CreateNewComment

# Create your views here.

from django.http import HttpResponse
from .models import MovieList, Movie, DiscussionPost, Comment
def about(response):
    return render(response, "main/about.html")

def profile(response):
    user = response.user
    return render(response, "main/profile.html",{"user":user})

def timeline(response):
    return render(response, "main/timeline.html")

def popular(response):
    return render(response, "main/popular.html")

def vote(response):
    return render(response, "main/vote.html")

def month(response, name):
    ls = MovieList.objects.get(name = "January Movies")
    return render(response, "main/month.html", {"ls":ls})

def movie(response, name, title):
    ls = MovieList.objects.all().get(name = name)
    movie = ls.movie_set.get(title = title)
    if response.method == "POST":
        form = CreateNewDiscussionPost(response.POST)
        if form.is_valid():
            p = form.cleaned_data["post"]
            t = DiscussionPost(post = p, movie = movie)
            t.save()
    else:
        form = CreateNewDiscussionPost()
    return render(response, "main/movie.html",{"ls":ls,"movie":movie, "form":form})

def home(response):
    ls = MovieList.objects.all()
    return render(response, "main/home.html", {"ls":ls})

def discussionposts(response, name, title):
    discussionposts = MovieList.objects.all().get(name = name).movie_set.get(title = title).discussionpost_set.all()
    return render(response, "main/discussionposts.html", {"discussionposts":discussionposts})

def discussionpost(response, name, title, id):
    discussionpost = MovieList.objects.all().get(name = name).movie_set.get(title = title).discussionpost_set.all().get(id = id)

    if response.method == "POST":
        form = CreateNewComment(response.POST)
        if form.is_valid():
            p = form.cleaned_data["comment"]
            t = Comment(comment = p, discussion_post = discussionpost)
            t.save()
    else:
        form = CreateNewComment()

    return render(response, "main/discussionpost.html", {"discussionpost":discussionpost, "form":form})