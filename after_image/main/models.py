from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class MovieList(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Movie(models.Model):
    movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    synopsis = models.CharField(max_length=5000)
    movie_likes = models.IntegerField(default = 0)
    image_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
#marjaneh
class DiscussionPost(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length = 100000)
    post_likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.post

class Comment(models.Model):
    discussion_post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 5000)

    def __str__(self):
        return self.comment
    
class Profile(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      bio = models.CharField(max_length= 1000)
      def __str__(self):
            return self.bio