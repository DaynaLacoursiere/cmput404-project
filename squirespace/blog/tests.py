# blank databases are created for tests and destroyed after tests are executed
# to keep test databases: python manage.py --keepdb
# test databases are prepended by test_ to their NAME

from django.test import TestCase, Client
from .models import Post, Comment
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
from django.core.urlresolvers import reverse
from friendship.models import Friend, Follow, FriendshipRequest

# test client is a python class that acts as a dummy web browser
# use for testing views
# test client does not need the server to be running
# use URL path not domain (to retrieve other pages you need urllib Python module)

c = Client()

class UserTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")

		c.login(username='John', password='a')	

	def testSquire(self):
		# ugly test to make sure squires exist
		self.assertEqual(self.user, self.user.squire.user)
		self.assertEqual(self.user.squire.hostname, "SquireSpace")

	def testUserViews(self):
		uuid1 = self.user.squire.theUUID
		profile = c.get('/profile/'+str(uuid1))
		self.assertEqual(profile.status_code, 301)  #200

		badurl = c.get('profile/123')
		# optional third argument for customized error messages
		self.assertEqual(badurl.status_code, 404, "wrong status code") 


class postTest(TestCase):	
	def setUp(self):	
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")

		c.login(username='John', password='a')	
		self.author = User.objects.get(username = "John")

		self.tpost = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="PUBLIC")
		self.tpost.save()

		self.tpost2 = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="FOAF")
		self.tpost2.save()

		self.tpost3 = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="FRIENDS")
		self.tpost3.save()

		self.tpost4 = Post.objects.create(author = self.author, title = "Test post please ignore", text = "yep", privatelevel="PRIVATE")
		self.tpost4.save()

# test methods must begin with test		
	def testCreatePost(self):
		author = User.objects.get(username = "John")
		self.assertTrue(isinstance(author, User))
		self.assertEqual(self.tpost.author, self.user)
		self.assertEqual(self.tpost.text, "yep")

	def testPrivacyLevel(self):
		self.assertEqual(self.tpost.privatelevel, 'PUBLIC')
		self.assertEqual(self.tpost2.privatelevel, 'FOAF')
		self.assertEqual(self.tpost3.privatelevel, 'FRIENDS')
		self.assertEqual(self.tpost4.privatelevel, 'PRIVATE')
	
	def testPostViews(self):
		uuid1 = self.tpost.id
		post1page = c.get('/post/'+str(uuid1))
		self.assertEqual(post1page.status_code, 301)  #200
		uuid2 = self.tpost2.id
		post2page = c.get("/post/"+str(uuid2))
		self.assertEqual(post2page.status_code, 301)  #404

		badurl = c.get('post/1')
		# optional third argument for customized error messages
		self.assertEqual(badurl.status_code, 404, "wrong status code") 

		response = c.get('/')
		self.assertEqual(response.status_code, 200)


class CommentModelTests(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")
		c.login(username='John', password='a')	
		post = Post.objects.create(author = self.user, title = "Test post please ignore", text = "yep")
		self.comment = Comment.objects.create(post = post, author = self.user, text = "commenttext")
		self.comment.save()

	def testCreateComment(self):
		self.assertIsNotNone(self.comment.post)
		self.assertEqual(self.comment.author, self.user)


# class FriendsTest(TestCase):
# 	def setUp(self):
# 		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")
# 		self.user2 = User.objects.create_user(username = "Jill", email = "jill@mailinator.com", password="b")

# 		c.login(username='John', password='a')	

# 	def testFriendRequest(self):
# 		Friend.objects.add_friend(self.user, self.user2, message = 'I would like to request your friendship.')
# 		self.assertTrue(self.user2 in Follow.objects.following(self.user))

# 	def testFriendAccept(self):
# 		for friend_request in Friend.objects.unrejected_requests(user=self.user):
# 			print "Accepting request"
# 			friend_request.accept();

# 		self.assertTrue(self.user2 in Friend.objects.friends(self.user))

	# def testUserViews(self):
	# 	uuid1 = self.user.squire.theUUID
	# 	profile = c.get('/profile/'+str(uuid1))
	# 	self.assertEqual(profile.status_code, 301)  #200

	# 	badurl = c.get('profile/123')
	# 	# optional third argument for customized error messages
	# 	self.assertEqual(badurl.status_code, 404, "wrong status code") 


