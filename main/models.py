from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from datetime import date


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    profile = models.CharField(max_length = 5000, default = "no bio")
    is_admin = models.BooleanField(default = False)
    username = models.CharField(max_length = 50)
    profile_photo = models.URLField(max_length=200, null=True, blank=True)
    
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# Create your models here.
class MovieList(models.Model):
    name = models.CharField(max_length=200)
    archived = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique = True)
    synopsis = models.CharField(max_length=5000)
    watched = models.IntegerField(default = 0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    release_date = models.IntegerField(default = 2000)
    length = models.IntegerField(default = 120)
    def __str__(self):
        return self.title

class DiscussionPost(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.CharField(max_length = 100000)
    post_likes = models.IntegerField(default = 0)


    def __str__(self):
        return self.post

class Comment(models.Model):
    discussion_post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 5000)

    def __str__(self):
        return self.comment

class Discussion_Likes(models.Model):
    discussion_post = models.ForeignKey(DiscussionPost, on_delete = models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    liked = models.BooleanField(default = False)

class Movie_Watched(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    month = models.ForeignKey(MovieList, on_delete = models.CASCADE)
    date_watched = models.DateField(default = date.today)
    watched = models.BooleanField(default = False)