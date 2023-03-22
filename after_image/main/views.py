from django.shortcuts import render, redirect
from .forms import CreateNewDiscussionPost, CreateNewComment, CreateNewBio
from django.contrib.auth.decorators import login_required


# Create your views here.

from django.http import HttpResponse
from .models import MovieList, Movie, DiscussionPost, Comment, MyUser, Movie_Watched, Discussion_Likes

@login_required
def about(response):
    return render(response, "main/about.html")

@login_required
def profile(response):
    user = response.user
    if response.method == "POST":
        form = CreateNewBio(response.POST)
        if form.is_valid():
            user.profile = form.cleaned_data["bio"]
    else:
        form = CreateNewBio()
    return render(response, "main/profile.html",{"user":user, "form":form})

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
    user = response.user
    try:
        watched = Movie_Watched.objects.get(user = response.user, month = ls, movie = movie)
    except Movie_Watched.DoesNotExist:
        watched = Movie_Watched(user = response.user, movie = movie, month = ls, watched = False)
        watched.save()
    if response.method == "POST":
        form = CreateNewDiscussionPost(response.POST)
        if form.is_valid():
            p = form.cleaned_data["post"]
            t = DiscussionPost(post = p, movie = movie, user = response.user)
            t.save()
    else:
        form = CreateNewDiscussionPost()
    return render(response, "main/movie.html",{"ls":ls,"movie":movie,"watched":watched,"name":name,"title":title, "form":form})

@login_required
def toggle_watched(response, name, title):
    ls = MovieList.objects.all().get(name = name)
    movie = ls.movie_set.get(title = title)
    user = response.user
    try:
        watched = Movie_Watched.objects.get(user = response.user, movie = movie, month = ls)
        watched.watched = not watched.watched
        watched.save()
        if watched.watched == True:
            movie.watched += 1
            movie.save()
        else:
            movie.watched -= 1
            movie.save()
    except Movie_Watched.DoesNotExist:
        watched = Movie_Watched(user = response.user, movie = movie, month = ls, watched = False)
        watched.save()
    
    return redirect('/movie/' + name +  '/' + title)
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
    try:
        liked = Discussion_Likes.objects.get(user = response.user, discussion_post = discussionpost)
    except Discussion_Likes.DoesNotExist:
        liked = Discussion_Likes(user = response.user, discussion_post = discussionpost, liked = False)
        liked.save()
    if response.method == "POST":
        form = CreateNewComment(response.POST)
        if form.is_valid():
            p = form.cleaned_data["comment"]
            t = Comment(comment = p, discussion_post = discussionpost, user = response.user)
            t.save()
    else:
        form = CreateNewComment()

    return render(response, "main/discussionpost.html", {"discussionpost":discussionpost, "form":form, "movie": movie, "name":name, "title":title, "id":id, "liked":liked})

@login_required
def toggle_likes(response, name, title, id):
    discussionpost = MovieList.objects.all().get(name = name).movie_set.get(title = title).discussionpost_set.all().get(id = id)
    try:
        liked = Discussion_Likes.objects.get(user = response.user, discussion_post = discussionpost)
        liked.liked = not liked.liked
        liked.save()
        if liked.liked == True:
            discussionpost.post_likes += 1
            discussionpost.save()
        else:
            discussionpost.post_likes -= 1
            discussionpost.save()
    except Discussion_Likes.DoesNotExist:
        liked = Discussion_Likes(user = response.user, discussion_post = discussionpost, liked = False)
        liked.save()
    id_string = str(id)
    return redirect('/movie/' + name +  '/' + title + '/discussionposts/' + id_string)