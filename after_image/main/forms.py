from django import forms

class CreateNewDiscussionPost(forms.Form):
    post = forms.CharField(label = "Post", max_length = 100000)

class CreateNewComment(forms.Form):
    comment = forms.CharField(label = "Comment", max_length = 10000)
