from django.test import TestCase, Client
from django.db import IntegrityError
from .models import *
from .views import *
from .forms import *
from .urls import *
from django.urls import reverse
from django.contrib.auth.models import User

class InitialRegisterOrLoginViewTestCase(TestCase):
    def testInitialHomeFirstTime(self):
        response = self.client.get(reverse('initial_register_or_login'))
        self.assertEqual(response.status_code, 200)

    def testRegisterLoginTemplate(self):
        response = self.client.get(reverse('initial_register_or_login'))
        self.assertTemplateUsed(response, 'main/initial_register_or_login.html')

class MonthViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.MyUser = MyUser.objects.create_user(username='username', email='user@gmail.com', password='password')
        self.movie_list = MovieList.objects.create(name="March Movies", archived=False)

    def test_month_view(self):
        self.client.login(email='user@gmail.com', password='password')
        url = reverse("month", args=[self.movie_list.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/month.html")
        self.assertEqual(response.context["ls"].name, self.movie_list.name)
        self.assertEqual(response.context["ls"].archived, self.movie_list.archived)

class PopularViewTest(TestCase):
    def setUp(self):
        self.MyUser = MyUser.objects.create_user(username='username', email='user@gmail.com', password='password')
        self.movie_list = MovieList.objects.create(name='January Movies')
        self.movie1 = Movie.objects.create(title='Red Deer', watched=True, movie_list=self.movie_list)
        self.movie2 = Movie.objects.create(title='Close', watched=False, movie_list=self.movie_list)
        self.discussion1 = DiscussionPost.objects.create(movie=self.movie1, user=self.MyUser, post='Awesome movie etc', post_likes=9)
        self.discussion2 = DiscussionPost.objects.create(movie=self.movie2, user=self.MyUser, post='Another Awesome movie etc', post_likes=6)
    
    def test_popular_view(self):
        self.client.login(email='user@gmail.com', password='password')
        url = reverse('popular')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('movie', response.context)
        self.assertIn('discussion', response.context)
        self.assertEqual(list(response.context['movie']), [self.movie2, self.movie1])
        self.assertEqual(list(response.context['discussion']), [self.discussion2, self.discussion1])


