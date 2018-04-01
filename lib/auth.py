import cookielib
from exceptions import AuthError
from request import Request

class Auth:
	def __init__(self, url, method, restricted_url):
		self.url = url
		self.restricted_url = restricted_url
		self.cj = cookielib.CookieJar()
		self.payload = None
		self.method = method

	def authenticate(self):
		print "==== Logging in ===="

		if not self.payload:
			raise AuthError('Authentication payload was missing')

		http_request = Request(self.cj)
		http_request.send(self.url, self.method, self.payload)

		if http_request.get_code() != 200:
			raise AuthError('Invalid HTTP Code: %s' % http_request.get_body())

		self.cj = http_request.get_cookie_jar()

		if not self.test_auth():
			raise AuthError('Authentication failed, reponse was: %s' % http_request.get_body())

	def set_payload(self, payload):
		self.payload = payload

	def get_cookie_jar(self):
		return self.cj

	def test_auth(self):
		http_request = Request(self.cj)
		http_request.send(self.restricted_url)

		if http_request.get_code() == 200 and http_request.get_url() == self.restricted_url:
			print "==== Logged in successfuly ===="
			return True

		return False

	def change_cookie_value(self, name, value):
		print "Setting cookie: %s to value: %s" % (name, value)

		for cookie in self.cj:
			if name == cookie.name:
				cookie.value = value

