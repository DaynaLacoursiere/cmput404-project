from django.test import TestCase, Client
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
import base64
auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('tester:testpass'),
}

# Create your tests here.
c = Client()

class UserApiTest(TestCase):
	def setUp(self):
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
		req = c.get('/author/2',  **auth_headers)
		self.assertEqual(req.status_code, 404)

	def testUserApiPost(self):
		req = c.post('/author/', {"username":"xxz", "email":"xx@x.ca", "password":"abc"},  **auth_headers)
		self.assertEqual(req.status_code, 201) #201 is Created