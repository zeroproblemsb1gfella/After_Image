from django.db import models

from django.db import models

# Create your models here.
class MovieList(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Movie(models.Model):
	movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	synopsis = models.CharField(max_length=5000)

    
	def __str__(self):
		return self.title
