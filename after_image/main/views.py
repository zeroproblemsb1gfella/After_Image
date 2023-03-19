from django.shortcuts import render
from .forms import CreateNewDiscussionPost, CreateNewComment
from django.contrib.auth.decorators import login_required


# Create your views here.

from django.http import HttpResponse
from .models import MovieList, Movie, DiscussionPost, Comment

@login_required
def about(response):
    return render(response, "main/about.html")

@login_required
def profile(response):
    user = response.user
    return render(response, "main/profile.html",{"user":user})

@login_required
def timeline(response):
    return render(response, "main/timeline.html")

@login_required
def popular(response):
    return render(response, "main/popular.html")

@login_required
def vote(response):
    return render(response, "main/vote.html")

def initial_register_or_login(response):
    return render(response, "main/initial_register_or_login.html")

@login_required
def month(response, name):
    ls = MovieList.objects.get(name = "January Movies")
    return render(response, "main/month.html", {"ls":ls})

@login_required
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

@login_required
def home(response):
    ls = MovieList.objects.all()
    return render(response, "main/home.html", {"ls":ls})

@login_required
def discussionposts(response, name, title):
    discussionposts = MovieList.objects.all().get(name = name).movie_set.get(title = title).discussionpost_set.all()
    movie = MovieList.objects.all().get(name = name).movie_set.get(title = title)
    return render(response, "main/discussionposts.html", {"discussionposts":discussionposts, "movie":movie})

@login_required
def discussionpost(response, name, title, id):
    discussionpost = MovieList.objects.all().get(name = name).movie_set.get(title = title).discussionpost_set.all().get(id = id)
    movie = MovieList.objects.all().get(name = name).movie_set.get(title = title)

    if response.method == "POST":
        form = CreateNewComment(response.POST)
        if form.is_valid():
            p = form.cleaned_data["comment"]
            t = Comment(comment = p, discussion_post = discussionpost)
            t.save()
    else:
        form = CreateNewComment()

    return render(response, "main/discussionpost.html", {"discussionpost":discussionpost, "form":form, "movie": movie})