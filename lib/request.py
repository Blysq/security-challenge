import urllib
import urllib2

class Request:
	def __init__(self, cookie_jar_instance = None):
		self.cj = cookie_jar_instance
		self.user_agent = 'Crawler Challenge'
		self.response = None
		self.body = None

	def send(self, url, method = None, payload = None):
		self.response = None
		data = None

		if self.cj != None:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			opener.addheaders = [('User-agent', self.user_agent)]
			urllib2.install_opener(opener)

		if payload:
			data = urllib.urlencode(payload)

		req = urllib2.Request(url, data)

		if method:
			req.get_method = lambda: method

		self.response = urllib2.urlopen(req)
		self.body = self.response.read()

	def set_user_agent(self, user_agent):
		self.user_agent = user_agent

	def get_code(self):
		return self.response.code

	def get_body(self):
		return self.body

	def get_url(self):
		return self.response.geturl()

	def get_cookie_jar(self):
		return self.cj

	def get_header(self, name):
		return self.response.info().getheader(name)

	def encode_params(self, params):
		return urllib.urlencode(params)

