from bs4 import BeautifulSoup
from lib.rule import Rule

class SQLInjectionRule(Rule):
	def __init__(self):
		Rule.__init__(self)
		self.name = "apostrophe test"

	def test(self, request, body, url):
		parsed_html = BeautifulSoup(body, 'html.parser')
		forms = parsed_html.find_all('form')

		if len(forms) > 0:
			for form in forms:
				inputs = form.find_all('input')
				method = 'POST'

				if form['method']:
					method = form['method']

				if self.send_payload(request, inputs, method, url):
					return True

		return False

	def send_payload(self, request, inputs, method, url):
		payload = self.create_payload(inputs, "'")

		if payload:
			if method == "GET":
				url = "%s?%s" % (url, request.encode_params(payload))

			request.send(url, method)
			html_body = request.get_body()

			found_vulnerability = html_body.find('You have an error in your SQL syntax')

			if found_vulnerability != -1:
				return True

