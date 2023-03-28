<<<<<<< Updated upstream
from django.test import TestCase, Client
from django.db import IntegrityError
from .models import *
from .views import *
from .forms import *
from .urls import *
from django.urls import reverse
from django.contrib.auth.models import User

class MovieListTestCase(TestCase):

    def setUp(self):
        self.movie_list = MovieList.objects.create(name='My Movie List')

    def testMovieListString(self):
        self.assertEqual(str(self.movie_list), 'My Movie List')

    def testMovieListArchivedReg(self):
        self.assertFalse(self.movie_list.archived)

    def testMovieListArchived(self):
        self.movie_list.archived = True
        self.movie_list.save()
        self.assertTrue(self.movie_list.archived)

    def testMovieListArchivedFalse(self):
        self.movie_list.archived = False
        self.movie_list.save()
        self.assertFalse(self.movie_list.archived)

    def testMovieListNameAtMax(self):
        max_length = self.movie_list._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def tearDown(self):
        self.movie_list.delete()

class AboutViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.MyUser = MyUser.objects.create_user(username='username', email='user@gmail.com', password='password')
        self.url = reverse('about')

    def testAboutWhileLoggedIn(self):
        self.client.login(email='user@gmail.com', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'about')
    
class CreateNewDiscussionPostFormTestCase(TestCase):

    #Forms don't require setup

    def testValidDiscussionForm(self):
        form_data = {'post': 'Awesome Movie! etc etc'}
        form = CreateNewDiscussionPost(data=form_data)
        self.assertTrue(form.is_valid())

    def testEmptyDiscussionForm(self):
        form_data = {'post': ''}
        form = CreateNewDiscussionPost(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['post'], ['This field is required.'])
=======
from django.test import TestCase
from main.forms import CreateNewComment

class CreateNewCommentTestCases(TestCase):
    def test_valid_form(self):
        data = {'comment': 'Test Comment'}
        form = CreateNewComment(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_comment(self):
        data = {'comment': ''}
        form = CreateNewComment(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['This field is required.'])

    def test_long_comment(self):
        data = {'comment': 'a' * 10001}
        form = CreateNewComment(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['Ensure this value has at most 10000 characters (it has 10001).'])
>>>>>>> Stashed changes
