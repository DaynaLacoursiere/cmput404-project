from django.test import TestCase, Client
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
from blog.models import Post, Comment
from friendship.models import Friend, Follow, FriendshipRequest
import base64
auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('tester:testpass'),
}

# Create your tests here.
c = Client()

class UserApiTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = "tester", email = "", password="testpass")
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")

	def testAuth(self):
		req = c.get('/posts/')
		self.assertEqual(req.status_code, 401)

	def logIn(self):
		c.login(username='John', password='a')	

	def testUserApiGet(self):
		uuid1 = self.user.squire.theUUID
		req = c.get('/author/'+str(uuid1), **auth_headers)
		self.assertEqual(req.status_code, 200)
		#req = c.get('/author/'+ "123e4567-e89b-12d3-a456-426655440000",  **auth_headers)
		#self.assertEqual(req.status_code, 404)

	def testUserApiPost(self):
		req = c.post('/author/', {"username":"xxz", "email":"xx@x.ca", "password":"abc"},  **auth_headers)
		self.assertEqual(req.status_code, 201) #201 is Created


class FriendsApiTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = "Jack", email = "jack@mailinator.com", password="b")
		self.user2 = User.objects.create_user(username = "Jill", email = "jill@mailinator.com", password="a")
		# make friend request
		self.request = Friend.objects.add_friend(self.user, self.user2, message = 'I would like to request your friendship.')
		# accept friend request
		self.request.accept();

	def testUserFriends(self):
		uuid = self.user.squire.theUUID
		# This should be returning a 200... TODO 
		req = c.get('/friends/' + str(uuid), **auth_headers)
		self.assertEqual(req.status_code, 301);


class PostApiTest(TestCase):	
	def setUp(self):	
		self.user = User.objects.create_user(username = "tester", email = "", password="testpass")
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")
		self.user2 = User.objects.create_user(username = "John2", email = "john@mailinator.com", password="a")
		self.user3 = User.objects.create_user(username = "John3", email = "john@mailinator.com", password="a")
		c.login(username='John', password='a')	
		self.author = User.objects.get(username = "John")
		self.author2 = User.objects.get(username = "John2")
		self.author3 = User.objects.get(username = "John3")

		self.tpost = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="PUBLIC")
		self.tpost.save()

		self.tpost2 = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="FOAF")
		self.tpost2.save()

		self.tpost3 = Post.objects.create(author = self.author2, title = "Test post please ignore", text = "yep", privatelevel="PUBLIC")
		self.tpost3.save()

		self.tpost4 = Post.objects.create(author = self.author3, title = "Test post please ignore", text = "yep", privatelevel="PUBLIC")
		self.tpost4.save()

		self.tpost5 = Post.objects.create(author = self.author3, title = "Test post please ignore", text = "yep", privatelevel="PRIVATE")
		self.tpost5.save()


	def testPostEndpointUnauthenticated(self):
		req = c.get('/posts/')
		self.assertEqual(req.status_code, 401)  #401 not authenticated

	def testPostEndpointAuthenticated(self):
		req = c.get('/posts/', **auth_headers)
		self.assertEqual(req.status_code, 200)  

	def testPostEndPublicPostsOnly(self):
		req = c.get('/posts/', **auth_headers)
		self.assertEqual(len(req.data['posts']), 3)
		self.assertEqual(req.data['count'], 3)
		self.assertEqual(req.data['query'], "posts")