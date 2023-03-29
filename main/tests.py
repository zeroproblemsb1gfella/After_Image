from django.test import TestCase, Client
from django.db import IntegrityError
from .models import *
from .views import *
from .forms import *
from .urls import *
from django.urls import reverse
from django.contrib.auth.models import User
from main.forms import CreateNewComment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MovieList, Movie, Movie_Watched, DiscussionPost, Discussion_Likes

from main.forms import CreateNewBio
from main.models import MovieList, Movie

class MovieListTestCase(TestCase):

    def setUp(self):
        self.movie_list = MovieList.objects.create(name='March Movies')

    def testMovieListString(self):
        self.assertEqual(str(self.movie_list), 'March Movies')

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

    def testValidDiscussionForm(self):
        form_data = {'post': 'Awesome Movie! etc etc'}
        form = CreateNewDiscussionPost(data=form_data)
        self.assertTrue(form.is_valid())

    def testEmptyDiscussionForm(self):
        form_data = {'post': ''}
        form = CreateNewDiscussionPost(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['post'], ['This field is required.'])


class CreateNewCommentTestCases(TestCase):
    def testValid(self):
        data = {'comment': 'Test Comment'}
        form = CreateNewComment(data=data)
        self.assertTrue(form.is_valid())

    def testEmptyComment(self):
        data = {'comment': ''}
        form = CreateNewComment(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['This field is required.'])

    def testExceededComment(self):
        data = {'comment': 'a' * 10001}
        form = CreateNewComment(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['Ensure this value has at most 10000 characters (it has 10001).'])

class HomeViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.MyUser = MyUser.objects.create_user(username='username', email='user@gmail.com', password='password')
        self.url = reverse('home')

    def testHome(request):
        movie_lists = MovieList.objects.all()
        context = {'movie_lists': movie_lists,}
        return render(request, 'main/home.html', context)


class ToggleWatchedTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.movie_list = MovieList.objects.create(name='Test List')
        self.movie = Movie.objects.create(title='Test Movie', movie_list=self.movie_list)
        
    def testToggleWatched(self):
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.watched, 0)
        

class TestMovieView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpass')
        self.movielist = MovieList.objects.create(name="TestList")
        self.movie = Movie.objects.create(title="TestMovie", movie_list=self.movielist)
        self.discussionpost = DiscussionPost.objects.create(post="Test Post", movie=self.movie, user=self.user)
        self.url = reverse("movie", args=[self.movielist.name, self.movie.title])

    def testMovieView(self):
        self.client.login(username='testuser', email='testuser@gmail.com', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class CreateNewBioTestCases(TestCase):
    def testValid(self):
        data = {'bio': 'Test Bio'}
        form = CreateNewBio(data=data)
        self.assertTrue(form.is_valid())

    def testEmpty(self):
        data = {'bio': ''}
        form = CreateNewBio(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['bio'], ['This field is required.'])

    def testExceededBio(self):
        data = {'bio': 'a' * 1001}
        form = CreateNewBio(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['bio'], ['Ensure this value has at most 1000 characters (it has 1001).'])

class MovieTestCases(TestCase):
    def setUp(self):
        testList = MovieList.objects.create(name='Test List')
        Movie.objects.create(movie_list=testList, title='Test Movie', synopsis='Test Synopsis')

    def testMovieTitle(self):
        movie = Movie.objects.get(id=1)
        textField = movie._meta.get_field('title').verbose_name
        self.assertEqual(textField, 'title')

    def testMovieTitleLength(self):
        movie = Movie.objects.get(id=1)
        max_length = movie._meta.get_field('title').max_length
        self.assertEqual(max_length, 300)

    def testSynopsisName(self):
        movie = Movie.objects.get(id=1)
        textField = movie._meta.get_field('synopsis').verbose_name
        self.assertEqual(textField, 'synopsis')

    def testSynopsisLength(self):
        movie = Movie.objects.get(id=1)
        max_length = movie._meta.get_field('synopsis').max_length
        self.assertEqual(max_length, 5000)

    def testCorrectMovieTitle(self):
        movie = Movie.objects.get(id=1)
        expectedMovieTitle = f"{movie.title}"
        self.assertEqual(str(movie), expectedMovieTitle)


class DiscussionPostTests(TestCase): 
    def setUp(self):
        testList = MovieList.objects.create(name = "Test List")
        self.movie = Movie.objects.create(movie_list = testList, title = "Test Movie 1", synopsis = "This is a synopsis of Test Movie 1")
        self.user = MyUser.objects.create(email = "testemail@test.com", password = "test123", username = "evan")
        self.discussionPost = DiscussionPost.objects.create(movie = self.movie, user = self.user, post = "This is a discussion post created for testing.")

    def testDiscussionPostContents(self):
        expected = "This is a discussion post created for testing."
        self.assertEqual(str(self.discussionPost), expected)

    def testDiscussionPostMovieForeignKey(self):
        self.assertEqual(self.discussionPost.movie, self.movie)

    def testDiscussionPostUserForeignKey(self):
        self.assertEqual(self.discussionPost.user, self.user)

class CommentsTests(TestCase):
    def setUp(self):
        testList = MovieList.objects.create(name = "Test List")
        self.movie = Movie.objects.create(movie_list = testList, title = "Test Movie 1", synopsis = "This is a synopsis of Test Movie 1")
        self.user = MyUser.objects.create(email = "testemail@test.com", password = "test123", username = "evan")
        self.discussionPost = DiscussionPost.objects.create(movie = self.movie, user = self.user, post = "This is a discussion post created for testing.")
        self.comment = Comment.objects.create(discussion_post = self.discussionPost, user = self.user, comment = "This is a test comment.")

    def testValidComment(self):
        self.assertEqual(str(self.comment), "This is a test comment.")
    
    def testDiscussionPostComment(self):
        self.assertEqual(self.comment.discussion_post, self.discussionPost)

    def testCommentbyUser(self):
        self.assertEqual(self.comment.user, self.user)

class GoBackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('go_back')

    def testGoBackView(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/movie.html')
    
    def testGoBackForInvalidURL(self):
        response = self.client.get('/invalid_url/')
        self.assertEqual(response.status_code, 404)

class toggleLike(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testUsername', email='testUserEmail@gmail.com', password='testPassword')
        self.movie_list = MovieList.objects.create(name='testMovieList')
        self.movie = Movie.objects.create(title='testMovie', movie_list=self.movie_list)
        self.discussion_post = DiscussionPost.objects.create(post='testPost', movie=self.movie, user=self.user)
        self.url = reverse('toggle_likes', args=[self.movie_list.name, self.movie.title, self.discussion_post.id])

    def testingToggleLikeBTN(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        postLiked = Discussion_Likes.objects.get(user=self.user, discussion_post=self.discussion_post)
        self.assertEqual(postLiked.liked, 0) 

class testDiscussionPost(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testUsername', email='testUserEmail@gmail.com', password='testPassword')
        self.movie_list = MovieList.objects.create(name='testMovieList')
        self.movie = Movie.objects.create(title='testMovie', movie_list=self.movie_list)
        self.discussion_post = DiscussionPost.objects.create(post='testPost', movie=self.movie, user=self.user)
        self.comment = Comment.objects.create(comment='testPost', discussion_post=self.discussion_post, user=self.user)
        self.url = reverse('discussionpost', args=[self.movie_list.name, self.movie.title, self.discussion_post.id])

    def testDiscussionPostComment(self):
        self.client.login(username='testUsername', password='testPassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class testDiscussionPosts(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username='testUsername', email='testUserEmail@gmail.com', password='testPassword')
        self.movie_list = MovieList.objects.create(name='testMovieList')
        self.movie = Movie.objects.create(title='testMovie', movie_list=self.movie_list)
        self.discussion_post = DiscussionPost.objects.create(post='testPost', movie=self.movie, user=self.user)
        self.url = reverse('discussionposts', args=[self.movie_list.name, self.movie.title])

    def testDiscussionPosts(self):
        self.client.login(username='testUsername', password='testPassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

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

    def testMonthView(self):
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

    def testPopularView(self):
        self.client.login(email='user@gmail.com', password='password')
        url = reverse('popular')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('movie', response.context)
        self.assertIn('discussion', response.context)
        self.assertEqual(list(response.context['movie']), [self.movie2, self.movie1])
        self.assertEqual(list(response.context['discussion']), [self.discussion2, self.discussion1])

class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.MyUser = MyUser.objects.create_user(username='username', email='user@gmail.com', password='password')
        self.url = reverse('profile')

    def testProfileWhileLoggedIn(self):
        self.client.login(email='user@gmail.com', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')
        self.assertContains(response, 'profile')

class DiscussionLikes(TestCase):
    def setUp(self):
        self.testList = MovieList.objects.create(name = "April Movies")
        self.movie = Movie.objects.create(movie_list = self.testList, title = "Test Movie", synopsis = "This is a synopsis of a Test Movie")
        self.user = MyUser.objects.create(email = "test@gmail.com", password = "test123", username = "hamza")
        self.discussionPost = DiscussionPost.objects.create(movie = self.movie, user = self.user, post = "This is a discussion post created for testing.")
        self.discussionLikes = Discussion_Likes.objects.create(user = self.user, discussion_post = self.discussionPost, liked = True)
        
    def testPostLikedByUser(self):
        self.assertTrue(self.discussionLikes.liked)
    
    def testUserWhoLiked(self):
        self.assertEquals(self.discussionLikes.user, self.user)
    
    def testWhichDiscussionPostIsLiked(self):
        self.assertEquals(self.discussionLikes.discussion_post, self.discussionPost)
        
class MovieWatched(TestCase):
    def setUp(self):
        self.testList = MovieList.objects.create(name = "April Movies")
        self.movie = Movie.objects.create(movie_list = self.testList, title = "Test Movie", synopsis = "This is a synopsis of a Test Movie")
        self.user = MyUser.objects.create(email = "test@gmail.com", password = "test123", username = "hamza")
        self.movieWatched = Movie_Watched(movie = self.movie, user = self.user, month = self.testList, watched = True)
    
    def testIsMovieWatched(self):
        self.assertTrue(self.movieWatched.watched)

    def testWhichMovieIsWatched(self):
        self.assertEquals(self.movieWatched.movie, self.movie)
    
    def testWhichUserWatchedMovie(self):
        self.assertEquals(self.movieWatched.user, self.user)
    
    def testWhichMonthIsMovieWatched(self):
        self.assertEquals(self.movieWatched.month, self.testList)
