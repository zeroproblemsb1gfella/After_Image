from django import forms
from main.models import Movie_Watched
class CreateNewDiscussionPost(forms.Form):
    post = forms.CharField(label = "Post", max_length = 100000)

class CreateNewComment(forms.Form):
    comment = forms.CharField(label = "Comment", max_length = 10000)

class CreateNewBio(forms.Form):
    bio = forms.CharField(label = "Bio", max_length = 1000)